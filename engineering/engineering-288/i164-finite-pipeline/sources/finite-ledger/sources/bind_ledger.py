"""Bind mechanical duties to the actual saved candidate; never discharge them."""
from expand_candidate import *
from verify_expansion import expected_counts
DUTIES=('SOURCE-OWNERSHIP','DECLARATION-RECORD-JOINS','EXPOSURE','COALITION-VISIBILITY','SOURCE-ESTABLISHED-LINKAGE','CANONICAL-ENCODING','PROTECTED-ACTOR-INFORMATION','OBSERVED-COUNTEREXAMPLES')
def check_binding(binding,identity,contract_hash):
 need(binding['model_sha256']==identity['model_sha256'],'stale model binding')
 need(binding['contract_sha256']==contract_hash,'stale contract binding')
 need(binding['qualification_established'] is False and binding['actual_admission'] is False,'dishonest qualification/admission')
 need(binding['equality_stream_sha256'] is None and binding['textual_stream_sha256'] is None,'uncomputed stream identity claimed')
 return True

def build(p):
 identity=load(R/'candidate/identity.json');verified=load(R/'results/expanded-verification.json')
 coverage={}
 for name,slots in [('EXECUTOR-STATUS',1024),('EXECUTOR-BACKUP',130),('EXECUTOR-STATE-ENTRY',65536),('ALLOWANCE-CHARGE',1154),('ALLOWANCE-STATE',1155)]:
  fields=[x for x in p['new_fields'] if x['record']==name]
  need(fields and all(x['slots']==slots for x in fields),'repetition directory mismatch '+name)
  for x in fields:
   for ctx in CONTEXTS:need(len(p['groups'][x['node_id'],ctx])==slots,'repetition token coverage')
  coverage[name]={'slots_per_context':slots,'fields':len(fields),'contexts':CONTEXTS,'witness_65_covered':slots>=65}
 save(R/'results/repetition-coverage.json',{'result':'PASS-REVISED-REPETITION-COVERAGE','coverage':coverage,'preserved_witness_sha256':sha(R/'repetition-witness/results/witness.json'),'charged_witness_sha256':sha(R/'results/accounting.json'),'actual_admission':False})
 need(verified['saved_model']['saved_bytes_sha256']==identity['model_sha256'],'missing saved-model verification')
 need(verified['structural']['rows']==identity['structural_edges']-8439026,'structural verification join')
 old_duties=[json.loads(x) for x in (R/'sources/model-duty-ledger.jsonl').read_bytes().splitlines()]
 oldrows=load(R/'retained/registers/fields.json');slots={r['node_id']:r['slots'] for r in oldrows}
 basecounts=[x['expanded_structural_occurrences'] for x in old_duties];need(sum(basecounts)==4368254,'historical duty coverage')
 oldcounts=basecounts+[2*max(slots[r['from_node']],slots[r['to_node']]) for r in p['rels'][len(basecounts):p['old_rel_n']]]
 need(sum(oldcounts)==8439026,'historical extension coverage')
 added=expected_counts(p);before=0;after=8439026
 d=R/'candidate/ledger';d.mkdir(exist_ok=True)
 with gzip.open(d/'structural-duties.jsonl.gz','wb',compresslevel=1) as f:
  for i,r in enumerate(p['rels']):
   old=oldcounts[i] if i<len(oldcounts) else 0;new=added[i];ranges=[]
   if old:ranges.append([before,before+old]);before+=old
   if new:ranges.append([after,after+new]);after+=new
   row={'relation_ordinal':i+1,'relation_sha256':H(W(r)+b'\n'),'required_structural_count':old+new,'edge_ranges':ranges,'source_binding':'relation-rules.json:'+str(i+1),'disposition':'NOT-ESTABLISHED','classification':'UNAVAILABLE','qualification':'UNAVAILABLE'}
   if i<len(old_duties):row['historical_duty_sha256']=H(W(old_duties[i])+b'\n')
   f.write(W(row)+b'\n')
 need(before==8439026 and after==identity['structural_edges'],'complete structural ranges')
 with gzip.open(d/'node-duties.jsonl.gz','wb',compresslevel=1) as f:
  tokens=0
  for i,node in enumerate(p['nodes']):
   ranges=[]
   for ctx in CONTEXTS:
    for start,seq,new in p['groups'][node['node_id'],ctx].parts:ranges.append([start,start+len(seq)]);tokens+=len(seq)
   f.write(W({'surface_ordinal':i+1,'field_class':node['node_id'],'token_ranges':ranges,'exact_duties':list(DUTIES),'exposure':'UNKNOWN' if i>=4119 else 'RETAINED','classification':'UNAVAILABLE','disposition':'NOT-ESTABLISHED','qualification':'UNAVAILABLE'})+b'\n')
 need(tokens==identity['tokens'],'complete node ranges')
 binding={'format':'I164-MECHANICAL-LEDGER-BINDING-1','model_sha256':identity['model_sha256'],'contract_sha256':sha(R/'records/expanded-contract.json'),'expanded_verification_sha256':sha(R/'results/expanded-verification.json'),'duties':{p.name:sha(p) for p in sorted(d.glob('*.gz'))},'relations':len(p['rels']),'surfaces':len(p['nodes']),'tokens':tokens,'structural_edges':after,'potential_pair_count':identity['equality_stream']['rows'],'potential_coverage':'entire i<j token domain under exact retained predicate; no enumerated stream claim','equality_stream_sha256':None,'textual_stream_sha256':None,'non_vacuity':'UNESTABLISHED; source/model coverage does not satisfy NV1-NV4','budgets':'UNAVAILABLE; pilot operation limits are not computational-risk allocations','qualification_established':False,'actual_admission':False}
 check_binding(binding,identity,sha(R/'records/expanded-contract.json'));save(d/'binding.json',binding)
 profile={'format':'I164-ACCOUNTED-PROFILE-BINDING-1','model_sha256':identity['model_sha256'],'model_bytes':identity['model_bytes'],'parent_model_sha256':'8aeab1b1990df99f2e2df1b6502a1f9f24a1cd06618d1ba3823d40419c96d189','contract_sha256':binding['contract_sha256'],'ledger_binding_sha256':sha(d/'binding.json'),'procedures':{n:sha(R/'code'/n) for n in ['allowances.py','executor_accounted.py','integration_accounted.py','producer_accounted.py','accountctl.py','expand_candidate.py','verify_expansion.py','check_edges.cpp','bind_ledger.py']},'approval_sha256':sha(R/'records/approval.json'),'relationships_43_sha256':sha(R/'retained/mapping/records/relationships-43.json'),'qualification_established':False,'actual_admission':False}
 save(R/'candidate/profile-binding.json',profile);return binding
if __name__=='__main__':
 import argparse
 ap=argparse.ArgumentParser();ap.add_argument('--parent',required=True);ap.add_argument('--base',required=True);a=ap.parse_args();p=prepare(a.parent,a.base);print(json.dumps(build(p)))
