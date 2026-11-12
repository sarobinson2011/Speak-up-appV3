"""Read-only reconciliation; never execute the author harness or candidate."""
from bytes_only import *
from collections import Counter
import ast
F=B/'author-results';T=B/'author-timeout';S=B/'source'
def jl(p):return [json.loads(x) for x in p.read_text().splitlines()]
def streams(f):
 chunks=[read(p) for p in sorted((f/'chunks').glob('*.json'))]
 for stream in ('stdout','stderr'):
  parts=[]
  for c in chunks:
   safe(c['path']);b=(f/c['path']).read_bytes();assert ident(b)=={k:c[k] for k in ('bytes','sha256')}
   if c['stream']==stream:parts.append(b)
  assert b''.join(parts)==(f/(stream+'.log')).read_bytes()
 assert {c['path'] for c in chunks}=={p.relative_to(f).as_posix() for p in (f/'chunks').glob('*.bin')}
 return len(chunks)
def main():
 src=fid(B/'host/inputs/I164-res-null-test-1-source.zip');assert src=={k:read(T/'SOURCE.json')[k] for k in ('bytes','sha256')}
 f=T/'attempt-1';rows=jl(f/'raw/progress.jsonl');old=[read(p) for p in sorted((f/'raw').glob('[0-9][0-9][0-9][0-9].json'))]
 assert old==rows==jl(f/'stdout.log') and len(old)==145 and [r['sequence'] for r in old]==list(range(1,146))
 assert Counter(x['status'] for x in old)=={'PASS':81,'REJECTED':64}
 assert not (f/'raw/RESULT.json').exists() and not (f/'raw/FAILURE.json').exists()
 ex=read(f/'exit.json');assert ex['returncode']==-9 and ex['timed_out'] is True and ex['automatic_retry'] is False and streams(f)==146
 assert read(f/'launch.json')['source_sha256']==src['sha256']
 plan=read(F/'harness/FULL-PLAN.json');assert len(plan)==316 and [x['original_sequence'] for x in plan]==list(range(1,317))
 code=(S/'tests/focused.py').read_text();tree_=ast.parse(code);calls={(n.lineno,n.col_offset):n for n in ast.walk(tree_) if isinstance(n,ast.Call) and isinstance(n.func,ast.Name) and n.func.id in ('check','reject')}
 for x in plan:
  n=calls[x['callsite']['line'],x['callsite']['column']]
  assert hashlib.sha256(ast.dump(n,include_attributes=False).encode()).hexdigest()==x['assertion_AST_sha256']
  assert ast.get_source_segment(code,n)==x['original_call_source']
 for r,p in zip(old,plan):assert all(r[k]==p[k] for k in ('name','layer')) and r['sequence']==p['original_sequence']
 for n,pin in read(F/'harness/HARNESS-MANIFEST.json').items():assert fid(F/'harness'/n)==pin
 specs=read(F/'harness/BATCH-PLAN.json');assert specs['source_test_identity']==fid(S/'tests/focused.py')
 indices=[];new=[];batches=[]
 for spec in specs['batches']:
  f=F/'batches'/spec['id'];raw=f/'raw';res=read(raw/'RESULT.json');rs=jl(raw/'progress.jsonl');so=jl(f/'stdout.log')
  assert rs==[read(p) for p in sorted(raw.glob('[0-9][0-9][0-9][0-9].json'))]==so[:-1] and so[-1]=={'event':'RESULT','result':res}
  assert [x['sequence'] for x in rs]==list(range(1,len(rs)+1)) and [x['original_sequence'] for x in rs]==spec['sequences']==res['original_sequences']
  for r in rs:
   p=plan[r['original_sequence']-1];assert all(r[k]==p[k] for k in ('name','layer','case','callsite','assertion_AST_sha256'))
  counts=Counter(x['status'] for x in rs);assert res['counts']==dict(PASS=counts['PASS'],REJECTED=counts['REJECTED'],FAIL=0) and res['result']=='PASS' and res['rows']==len(rs)
  exb=read(f/'exit.json');assert exb['returncode']==0 and exb['timed_out'] is False and exb['automatic_retry'] is False
  chunks=streams(f);assert chunks==exb['captured_chunks']
  assert fid(f/'setup-state.json')==read(f/'setup-state-identity.json')
  if batches:
   consumed=read(f/'consumed-state.json');assert consumed['identity']==batches[-1]['setup_identity']
  indices+=spec['sequences'];new+=rs;batches.append({'batch':spec['id'],'rows':len(rs),'counts':dict(counts),'exit':exb,'chunks':chunks,'setup_identity':fid(f/'setup-state.json'),'setup_credit':res['setup_credit']})
 assert indices==list(range(146,317)) and len(new)==171 and Counter(x['status'] for x in new)=={'PASS':54,'REJECTED':117}
 combined=[{'group':'attempt-1','layer':x['layer'],'name':x['name'],'original_sequence':x['sequence'],'status':x['status']} for x in old]
 for batch in specs['batches']:
  for r in new:
   if r['original_sequence'] in batch['sequences']:combined.append({'group':'continuation','layer':r['layer'],'name':r['name'],'original_sequence':r['original_sequence'],'status':r['status'],'case':r['case'],'callsite':r['callsite']})
 assert combined==read(F/'COMBINED-INDEX.json')
 save(B/'focused-record-audit.json',{'status':'PASS','source':src,'timeout_attempt':{'corroborated_rows':145,'counts':{'PASS':81,'REJECTED':64},'exit':ex,'chunks':146,'final_RESULT':'MISSING','child_FAILURE':'MISSING','campaign_status':'TIMED_OUT_INCOMPLETE'},'continuation':{'corroborated_rows':171,'counts':{'PASS':54,'REJECTED':117},'batches':batches,'layers':dict(Counter(x['layer'] for x in new))},'unique_plan_coverage':{'rows':316,'PASS':135,'REJECTED':181,'not_one_successful_campaign':True},'original_assertion_ASTs_match_fixed_source':True,'individual_progress_stdout_exact':True,'setup_credit':0,'completed_checks_replayed_by_review':0,'full_public_negative_derivations':0})
 print('145 timeout rows + 171 separate continuation rows reconciled; no replay',flush=True)
if __name__=='__main__':
 try:main();save(B/'focused-record-audit-corrected.exit.json',{'exit':0})
 except BaseException as e:save(B/'focused-record-audit-corrected.exit.json',{'exit':1,'failure':repr(e)});raise
