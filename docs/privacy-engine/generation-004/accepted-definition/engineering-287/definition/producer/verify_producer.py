"""Bounded checks of documentary producer construction, with synthetic work states."""
from pathlib import Path
import csv,json,runpy
O=Path(__file__).resolve().parents[1];ns=runpy.run_path(str(O/'producer/dependency_rules.py'))
def rows(p):return list(csv.DictReader((O/p).open(),delimiter='\t'))
req=ns['requirements'];ready=ns['readiness'];cases=0
work=rows('privacy/producer-proposal/dependencies.tsv');ids={r['work_id'] for r in work}
expected=[]
for phase in ns['PHASES']:
 for w in ids:
  if phase not in ns['allowed_phases'](w):
   try:req(w,phase)
   except ValueError:pass
   else:raise AssertionError('wrong phase accepted')
   continue
  for k,p in req(w,phase,('history','state')):
   assert k in ('WORK','EVIDENCE')
   if k=='WORK':assert p in ids
   expected.append((phase,w,k,p,'WHEN-HISTORY-AVAILABLE' if w=='joint-view' and p=='history-validate' else 'WHEN-STATE-AVAILABLE' if w=='joint-view' and p=='state-validate' else 'REQUIRED'))
  for avail in ((),('history',),('state',),('history','state')):
   rr=req(w,phase,avail);states={p:'DONE' for k,p in rr if k=='WORK'};evidence={p:'DONE' for k,p in rr if k=='EVIDENCE'}
   result=ready(w,phase,states,evidence,avail);assert result['dependency_state']=='READY-FOR-SOURCE-WORK' and result['protocol_permission'] is False;cases+=1
   for k,p in rr:
    state2=dict(states);ev2=dict(evidence);target=state2 if k=='WORK' else ev2;target.pop(p)
    assert ready(w,phase,state2,ev2,avail)['dependency_state']=='UNRESOLVED';cases+=1
    target[p]='FAILED';assert ready(w,phase,state2,ev2,avail)['dependency_state']=='FAILED';cases+=1
assert set(expected)=={tuple(r[k] for k in ('phase','work_id','predecessor_kind','predecessor','condition')) for r in rows('producer/dependency-edges.tsv')}
assert req('proof-artifacts','VERIFICATION')==[('EVIDENCE','verifier-input-basis')]
assert req('phase-bind','E')==[('WORK','fix-rc')]
assert req('phase-bind','PRE-EXECUTION')==[('EVIDENCE','authorization-basis')]
assert ('WORK','state-validate') not in req('joint-view','PRE-EXECUTION',('history',))
assert ('WORK','history-validate') not in req('joint-view','PRE-EXECUTION',('state',))
assert ('WORK','joint-view') not in req('component-produce','AUTHORIZED')
assert ready('final-gate-write','PRE-COMMITMENT',{'prepare-intent':'DONE','component-produce':'DONE'},{})['dependency_state']=='UNRESOLVED'
# No documentary temporal cycle: V qualification is independent; static work does not await real U.
adj={w:set() for w in ids}
for _,w,k,p,_ in expected:
 if k=='WORK':adj[w].add(p)
def visit(w,path):
 assert w not in path,'Dependency cycle: '+str(path+[w])
 for p in adj[w]:visit(p,path+[w])
for w in ids:visit(w,[])
fields=rows('profile/fragments/fields.tsv');directory=rows('privacy/producer-proposal/evidence-fields.tsv')
for f in fields:
 expected_records=sorted({r['record'] for r in directory if f['field_id'] in r['consumer_fields'].split(';')})
 assert ns['consumed_records'](f['field_id'])==expected_records and expected_records
matrix=ns['custody_matrix']();assert matrix==rows('producer/custody-fields.tsv')
assert all(r['visibility']=='UNKNOWN' and r['context_scope']=='BOTH-POTENTIAL' and r['role_is_appointed_actor']=='FALSE' for r in matrix)
oldnodes={r['node_id']:r for r in rows('privacy/model/nodes.tsv')};newnodes={r['node_id']:r for r in rows('producer/augmented-nodes.tsv')}
assert all(newnodes[n]==r for n,r in oldnodes.items())
def edges(path):return {tuple(r[k] for k in ('from_node','to_node','relation')) for r in rows(path)}
oldedges=edges('privacy/model/structural-edges.tsv');newedges=edges('producer/augmented-edges.tsv');assert oldedges<=newedges
assert all(a in newnodes and b in newnodes for a,b,_ in newedges)
assert {('PRODUCER-EVIDENCE:'+r['record']+':'+r['field'],'PRODUCER-ROLE:'+r['role'],'POTENTIAL-CUSTODY') for r in matrix}<newedges
assert len(newedges)==len(rows('producer/augmented-edges.tsv'))
carrier=runpy.run_path(str(O/'producer/evidence_carrier.py'))
assert rows('producer/carrier-applicability.tsv')==[{'phase':p,'record':r,'field':f,'applicability':'REQUIRED-BYTES' if carrier['applicable'](r,f,p) else 'INAPPLICABLE-TAG' if p in carrier['RECORD_PHASES'][r] else 'INAPPLICABLE-RECORD'} for p in carrier['PHASES'] for r,fs in carrier['directory']().items() for f in fs]
for rec,fs in carrier['directory']().items():
 for field in fs:
  for tag in ('presence','length'):
   assert ('CARRIER-V2:'+rec+':'+field+':'+tag,'PRODUCER-EVIDENCE:'+rec+':'+field,'CARRIER-FRAMES') in newedges
original=rows('privacy/model/unresolved-producer-conditions.tsv');resolved=rows('producer/condition-dispositions.tsv')
assert len(original)==len(resolved)==19
for a,b in zip(original,resolved):assert all(a[k]==b[k] for k in ('work_id','condition_node','exact_condition')) and b['resolution']
# The supplementary graph is an obligation inventory, not an admitted graph.
report={'status':'PASS-BOUNDED-PRODUCER-CONSTRUCTION','dependency_state_cases':cases,'condition_dispositions':19,'field_record_joins':len(fields),'potential_custody_cells':len(matrix),'all_inherited_nodes_edges_preserved':True,'visibility_established':False,'source_qualified':False,'profile_admitted':False,'phase_encoding_draft_constructed':True}
(O/'verification/producer-construction.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS — 19 producer conditions dispositioned; phase dependencies and missing-evidence failures checked.')
print('PASS — all 118 field-to-record joins; 841 potential custody cells remain UNKNOWN.')
print('PASS — augmented graph preserves every inherited node and edge; no privacy admission claimed.')
