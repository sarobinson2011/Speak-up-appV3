from pathlib import Path
import ast,datetime,hashlib,json,statistics
P=Path(__file__).resolve().parent;R=P/'source';H=P/'harness';H.mkdir(exist_ok=True)
def enc(x):return (json.dumps(x,indent=2,sort_keys=True)+'\n').encode()
def ident(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
raw=(R/'tests/focused.py').read_bytes();tree=ast.parse(raw);main=next(x for x in tree.body if isinstance(x,ast.FunctionDef) and x.name=='main')
calls={}
for x in ast.walk(main):
 if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id in ('check','reject'):
  calls[x.lineno]=x
assert len(calls)==len([x for x in ast.walk(main) if isinstance(x,ast.Call) and isinstance(x.func,ast.Name) and x.func.id in ('check','reject')])
old=[json.loads(f.read_bytes()) for f in sorted((P/'prior-results/attempt-1/raw').glob('[0-9][0-9][0-9][0-9].json'))]
plan=[]
def add(line,name,case):
 c=calls[line];layer=ast.literal_eval(c.args[2]) if len(c.args)>2 else ('pure source/model oracle; no authentication' if c.func.id=='check' else 'pure model constraints; no authenticated basis')
 entry={'original_sequence':len(plan)+1,'name':name,'layer':layer,'assertion_kind':c.func.id,'case':case,
 'callsite':{'file':'tests/focused.py','line':c.lineno,'column':c.col_offset,'end_line':c.end_lineno,'end_column':c.end_col_offset},
 'assertion_AST_sha256':hashlib.sha256(ast.dump(c,include_attributes=False).encode()).hexdigest(),
 'original_call_source':ast.get_source_segment(raw.decode(),c)}
 plan.append(entry)
prefix_lines=[45,47,48,54,55,59,60]+[62]*11+[64]+[66]*2+[68,69,70,72]+[75]*4+[76,80]+[83]*10+[84,86,87]
assert len(prefix_lines)==44
for i,line in enumerate(prefix_lines):add(line,old[i]['name'],{'group':'completed-prefix','ordinal':i+1})
fixtures=json.loads((R/'fixtures/retained-decref-cases.json').read_bytes())
for num,f in enumerate(fixtures):
 p=f['output']
 for branch in ('immortal','non-immortal-positive-gt-one'):
  case={'group':'matrix','fixture':num,'fixture_name':f['name'],'branch':branch,'context':p['scope']['context'],'control_completed':p['earlier_control_completed_in_model'],'failure_origin':p['failure_origin_region'],'C_NULL':p['res_value_role']['C_NULL'],'python_value_class':p['res_value_role']['python_value_class'],'fixture_identity':ident(enc(f))}
  for line,suffix in [(99,'normal comparison accepted'),(100,'independent outcome and preserved lineage oracle'),(101,'opposite comparison result')]:add(line,str(num)+'/'+branch+'/'+suffix,{**case,'stage':suffix})
assert len(plan)==188
add(105,'48 class variants cover both contexts prefixes origins fast branches and three result classes',{'group':'overall','stage':'matrix aggregate'})
def paths_at(line):
 node=next(n for n in ast.walk(main) if isinstance(n,ast.For) and n.lineno==line)
 return [ast.literal_eval(x.elts[0]) for x in node.iter.elts]
for ctx in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
 start=len(plan)
 def entry(line,label,stage):add(line,ctx+'/'+label,{'group':'per-context','context':ctx,'stage':stage})
 for premise in ('continuation','res_storage_continuity'):
  entry(110,premise+' unavailable has no outcome',{'premise':premise,'claim':'unavailable outcome'})
  entry(111,premise+' unavailable cannot compare',{'premise':premise,'claim':'false comparison'})
  entry(112,premise+' omitted cannot compare',{'premise':premise,'claim':'omitted premise'})
 for k in ('conditional_fast_completion_in_model','helper_c_return_completed_in_model','res_assignment_established','res_assignment','res_value_role'):
  entry(114,'missing predecessor '+k,{'predecessor_field':k})
 for index,frontiers in [(0,('raise','catchable-interruption','process-termination','unobserved')),(1,('interruption','process-termination','unobserved'))]:
  for frontier in frontiers:
   entry(118,str(index)+'/'+frontier,{'stage_index':index,'frontier':frontier,'claim':'legitimate'})
   entry(119,frontier+'/false outcome',{'stage_index':index,'frontier':frontier,'claim':'false outcome'})
 for index,path in enumerate(paths_at(120)):entry(121,'input '+repr(path),{'mutation_index':index,'path':list(path)})
 entry(123,'coordinated submitted lineage versus fixed selected input',{'claim':'coordinated lineage'})
 for index,path in enumerate(paths_at(124)):entry(125,'output '+repr(path),{'mutation_index':index,'path':list(path)})
 for index,path in enumerate(paths_at(126)):entry(127,'exact input '+repr(path),{'mutation_index':index,'path':list(path)})
 for index,path in enumerate(paths_at(128)):entry(129,'exact output '+repr(path),{'mutation_index':index,'path':list(path)})
 for line,label in [(130,'subclass literal key'),(132,'direct returned projection mutation'),(133,'pristine expectations isolated'),(135,'returned binding isolation')]:entry(line,label,{'claim':label})
 assert len(plan)-start==62
for line,label in [(137,'returned catalogue isolation'),(138,'new authentication paths remain unexecuted'),(139,'fixed source bytes unchanged after pass')]:add(line,label,{'group':'overall','stage':label})
assert len(plan)==316
for r,p in zip(old,plan):assert r['sequence']==p['original_sequence'] and r['name']==p['name'] and r['layer']==p['layer']
remaining=plan[145:];assert len(remaining)==171 and remaining[0]['name']=='16/non-immortal-positive-gt-one/opposite comparison result'
for name,value in [('FULL-PLAN.json',plan),('REMAINING-PLAN.json',remaining)]: (H/name).write_bytes(enc(value))
# Deadlines use the saved computation timings, not an assumed profiler diagnosis.
times=[datetime.datetime.fromisoformat(r['utc']) for r in old];deltas=[(b-a).total_seconds() for a,b in zip(times,times[1:])]
negative=[deltas[i-1] for i in range(1,len(old)) if old[i]['name'].endswith('/opposite comparison result')]
normal=[deltas[i-1] for i in range(1,len(old)) if old[i]['name'].endswith('/normal comparison accepted')]
batches=[
 {'id':'batch-01','sequences':[146],'mode':'matrix-initial','fixture_start':0,'fixture_stop':17,'deadline_seconds':900,'basis':'Reconstruct 34 model setups for the unfinished aggregate/representatives, without 101 completed matrix assertions; execute only row146. Bound exceeds 34 times saved maximum normal-plus-opposite timing plus setup margin.'},
 {'id':'batch-02','sequences':list(range(147,189)),'mode':'matrix-rest','fixture_start':17,'fixture_stop':24,'deadline_seconds':600,'basis':'Fourteen remaining matrix cases. Saved per-case normal/oracle/opposite intervals inform a roughly 250-second estimate; 600-second bound includes setup/recording headroom.'},
 {'id':'batch-03','sequences':list(range(189,252)),'mode':'context-one','deadline_seconds':900,'basis':'One aggregate plus 62 assertions, with saved representative inputs. Conservative 900-second bound permits multiple recursive model calls per assertion, informed by saved single negative durations.'},
 {'id':'batch-04','sequences':list(range(252,314)),'mode':'context-two','deadline_seconds':900,'basis':'62 assertions in second context; same saved-timing basis as batch03, no completed-assertion replay.'},
 {'id':'batch-05','sequences':list(range(314,317)),'mode':'overall','deadline_seconds':180,'basis':'Three remaining catalogue/guard/source controls, with retained setup; short bounded finalization.'}]
assert [i for b in batches for i in b['sequences']]==list(range(146,317))
(H/'BATCH-PLAN.json').write_bytes(enc({'batches':batches,'saved_timing_seconds':{'normal_check_delta_max':max(normal),'opposite_check_delta_max':max(negative),'opposite_check_delta_median':statistics.median(negative),'matrix_start_to_last_record':(times[-1]-times[43]).total_seconds()},'automatic_retry':False,'candidate_changed':False,'planned_assertions':316,'previous_corresponding_rows':145,'new_outstanding':171,'source_test_identity':ident(raw)}))
(H/'HARNESS-POLICY.txt').write_text('''One harness-only continuation of exactly original checks146–316. The pinned full plan maps repeated labels to original sequence, callsite, AST identity and case/stage. Original check/reject lambdas and the audit/profile guards remain unchanged. Candidate files are not edited. The dispatcher wraps original assertion calls only to skip completed or out-of-batch assertions and records original IDs. It never evaluates a skipped assertion lambda.

Earlier model setup is reconstructed only to supply original outstanding assertions, matrix aggregate and both representative contexts. Setup has no assertion credit. Model-produced coverage, occurrence IDs, catalogues and representatives are saved between batches with exact identities, not substituted expected results or authenticated bases. The original global profile guard remains enabled during model work; its overhead has not been isolated or removed. No public/authenticated constructed path is permitted.

Five bounded batches; stop on the first failed/partial batch, preserve it and do not retry. Checkpoint every batch. Final reconciliation must cover all316 original IDs with exactly the original145 plus these171, comparing raw rows, progress, stdout, exits and plan identities. The timeout/missing final records of attempt1 remain historical facts even if the logical check list later completes.
''')
print(json.dumps({'full':len(plan),'remaining':len(remaining),'first':remaining[0]['name'],'last':remaining[-1]['name'],'batches':[{'id':b['id'],'rows':len(b['sequences']),'deadline':b['deadline_seconds']} for b in batches],'timings':json.loads((H/'BATCH-PLAN.json').read_bytes())['saved_timing_seconds']},indent=2))
