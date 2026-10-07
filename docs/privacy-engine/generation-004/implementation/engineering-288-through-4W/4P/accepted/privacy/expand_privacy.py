"""Fresh static graph expansion. No historical code, appointment or admission.
Streams every equality pair; never substitutes sampled pairs or drops actor edges.
"""
from pathlib import Path
import csv,json,hashlib,itertools,struct,sys
O=Path(__file__).resolve().parents[1]
def rows(path):return list(csv.DictReader((O/path).open(),delimiter='\t'))
def canonical(value):return (json.dumps(value,sort_keys=True,separators=(',',':'),ensure_ascii=True)+'\n').encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def construct():
 surfaces=rows('producer/augmented-nodes.tsv');relations=rows('producer/augmented-edges.tsv');components=rows('profile/fragments/candidate-components.tsv')
 tokens=[];by={};contexts=['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO']
 for context in contexts:
  for surface in surfaces:
   sid=surface['node_id'];count=len(components) if sid.startswith('CORE:COMPONENT-BINDING.') else 1
   for record in range(1,count+1):
    fresh=sid.startswith('CORE:') and sid.split('.')[-1].replace('-','_')=='transition_occurrence_id'
    constant=surface['reuse']!='NONE'
    value='FRESH:'+context if fresh else 'CONSTANT:'+sid if constant else 'ARBITRARY'
    ident=context+'::'+sid+(f'::RECORD-{record:06}' if count>1 else '')
    t={'index':len(tokens),'id':ident,'surface':sid,'context':context,'record':record,'exposure':surface['declared_exposure'],'reuse':surface['reuse'],'arbitrary':not fresh and not constant,'symbolic_digest':sha(value.encode())}
    tokens.append(t);by.setdefault((context,sid),[]).append(t)
 # Keep distinct relation identities; replicate owning component bindings correctly.
 edges=[]
 def component(t):
  s=t['surface']
  if s.startswith('CORE:COMPONENT-0'):return int(s.split('COMPONENT-')[1].split('.')[0])
  if s.startswith('FIELD:PE-TSE-FIELD-COMPONENT-'):return int(s.split('COMPONENT-')[1].split('-')[0])
  return None
 for order,e in enumerate(relations,1):
  for context in contexts:
   for a in by[(context,e['from_node'])]:
    for b in by[(context,e['to_node'])]:
     if a['surface'].startswith('CORE:COMPONENT-BINDING.') and component(b) is not None and a['record']!=component(b):continue
     if b['surface'].startswith('CORE:COMPONENT-BINDING.') and component(a) is not None and b['record']!=component(a):continue
     edges.append([a['index'],b['index'],order,e['relation']])
 return surfaces,relations,tokens,edges

def equal_pairs(tokens):
 for a,b in itertools.combinations(tokens,2):
  # Retained S71: OR, not AND. Arbitrary-to-constant/fresh edges are also included.
  if a['arbitrary'] or b['arbitrary'] or a['symbolic_digest']==b['symbolic_digest']:yield a['index'],b['index']
def expand(materialize=False):
 surfaces,relations,tokens,edges=construct()
 # Canonical streamed edge member: domain separator then unsigned U32 indices.
 header=b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n';h=hashlib.sha256(header);count=0
 handle=(O/'privacy/expanded/equality-pairs.bin').open('wb') if materialize else None
 if handle:handle.write(header)
 try:
  for a,b in equal_pairs(tokens):
   row=struct.pack('>II',a,b);h.update(row);count+=1
   if handle:handle.write(row)
 finally:
  if handle:handle.close()
 # Independent count formula: excluded pairs contain no arbitrary endpoint and have unequal digests.
 fixed=[t for t in tokens if not t['arbitrary']];groups={}
 for t in fixed:groups[t['symbolic_digest']]=groups.get(t['symbolic_digest'],0)+1
 choose=lambda n:n*(n-1)//2
 expected=choose(len(tokens))-choose(len(fixed))+sum(choose(n) for n in groups.values())
 assert count==expected
 # One arbitrary endpoint links to every other token under the retained rule.
 assert any(t['arbitrary'] for t in tokens)
 for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
  for role in ('n','a','r'):assert any(t['id']==context+'::PUBLIC-PI:'+role and t['arbitrary'] for t in tokens)
 inputs={p:sha((O/p).read_bytes()) for p in ['producer/augmented-nodes.tsv','producer/augmented-edges.tsv','privacy/observation_correlation.py','privacy/cross_role_correlation.py','sources/PE-G4-SOURCE-S86.md','privacy/cross_role_uniqueness.py','sources/PE-G4-SOURCE-S87.md','privacy/public-relationship-binding-schema.tsv','profile/fragments/candidate-components.tsv']}
 payload={'format':'PE-G4-PRIVACY-INTEGRATION-CANDIDATE-V1','status':'UNADMITTED-CANDIDATE-NOT-GOVERNING-PRIVACY-MEMBER','input_sha256':inputs,'surfaces':surfaces,'relations':relations,'tokens':tokens,'structural_edges':edges,'equality_stream':{'format':'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1','row_encoding':'U32-BE left index; U32-BE right index','ordering':'lexicographic index pairs, i<j','predicate':'left.arbitrary OR right.arbitrary OR equal symbolic_digest','rows':count,'sha256':h.hexdigest(),'bytes':len(header)+8*count},'actor_graph_policy':'ALL structural and equality edges; no visibility/permission filtering','evidence_state':{'source_appointment':None,'privacy_appointment':None,'required_coalitions':None,'authenticated_visibility':None,'runtime_occurrences':None},'admission':False}
 raw=canonical(payload);target=O/'privacy/expanded/PRIVACY.candidate.json'
 if target.exists():assert target.read_bytes()==raw, 'Privacy candidate differs from exact regeneration'
 else:target.write_bytes(raw)
 report={'construction':'PASS-EXACT-DECLARATION-EXPANSION','contexts':2,'tokens':len(tokens),'structural_edges':len(edges),'potential_equality_edges':count,'equality_count_independently_checked':True,'actor_connected_components':1,'actor_safety_established':False,'unknown_exposure_tokens':sum(t['exposure']=='UNKNOWN' for t in tokens),'privacy_candidate_sha256':sha(raw),'governing_privacy_member_constructed':False,'profile_admitted':False,'static_obstruction':'S86/S87 conditionally correct cross-role correlation and uniqueness. All unqualified pairs, source-established paths and unknown evidence remain fail-closed.'}
 (O/'verification/privacy-expansion.json').write_bytes(canonical(report))
 return report
if __name__=='__main__':
 result=expand('--materialize' in sys.argv)
 print('PASS — two-context graph expanded; every conservative equality pair hashed and counted.')
 print('BOUNDARY — candidate privacy bytes are not an admitted PRIVACY member; cross-role public equality remains unpermitted.')
 print(json.dumps({k:result[k] for k in ('tokens','structural_edges','potential_equality_edges','unknown_exposure_tokens')}))
