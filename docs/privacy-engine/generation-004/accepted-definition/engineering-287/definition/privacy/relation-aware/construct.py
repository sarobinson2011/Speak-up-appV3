"""Obligation construction only. Never an admission or cryptographic proof checker."""
from pathlib import Path
import hashlib,json,runpy
O=Path(__file__).resolve().parents[2]
P=21888242871839275222246405745257275088548364400416034343698204186575808495617

def scalar(x):
 return type(x) is int and 0<=x<P

def collision_reduction(left,right,left_output,right_output):
 """Check conditional tuple reasoning; does NOT evaluate Poseidon or verify a proof."""
 if not all(type(t) is tuple and len(t)==3 and all(scalar(x) for x in t) for t in (left,right)) or not all(scalar(x) for x in (left_output,right_output)):
  raise ValueError('noncanonical scalar tuple')
 if left[2]!=right[2]:raise ValueError('different SIGN_DOMAIN relation')
 if left[1]==right[1]:return 'SAME-ACTION-NO-CROSS-ACTION-REDUCTION'
 if left_output!=right_output:return 'OUTPUTS-DIFFER'
 assert left!=right
 return 'IF-BOTH-OUTPUTS-ARE-VALID-THEN-HASH-COLLISION'

def construct():
 X=runpy.run_path(str(O/'privacy/expand_privacy.py'))
 surfaces,relations,tokens,edges=X['construct']()
 model=json.loads((O/'privacy/expanded/PRIVACY.candidate.json').read_text())
 if model['tokens']!=tokens or model['structural_edges']!=edges or model['surfaces']!=surfaces or model['relations']!=relations:
  raise ValueError('stale static declaration')
 paths=['sources/retained/S22.md','sources/retained/S71.md','privacy/expanded/PRIVACY.candidate.json','privacy/relation-aware/rule.md','privacy/relation-aware/construct.py']
 return {
  'format':'PE-G4-RELATION-OBLIGATIONS-V1',
  'input_sha256':{x:hashlib.sha256((O/x).read_bytes()).hexdigest() for x in paths},
  'scope':'PROPOSED-STATIC-RULE-NOT-GOVERNING-PRIVACY',
  'full_graph':{'tokens':len(tokens),'structural_edges':len(edges),'equality_stream':model['equality_stream'],'removed_nodes':0,'removed_edges':0},
  'pair':['SYMBOLIC-U-ONE::PUBLIC-PI:n','SYMBOLIC-U-TWO::PUBLIC-PI:n'],
  'branches':[
   {'condition':'a1=a2','rule':'S84 SAME-SCOPED-A-N only; all other paths retained'},
   {'condition':'a1!=a2 AND n1!=n2','rule':'No direct n equality; all other paths retained'},
   {'condition':'a1!=a2 AND n1=n2','rule':'Conditional collision reduction; proof soundness, exact algorithm, security budget, unlinkability and whole-view obligations OPEN'}],
  'all_other_pairs':'RETAINED; no discharge granted by this manifest',
  'established_cross_action_equality':'REJECT',
  'unknown_visibility':'REJECT',
  'actor_graph':'COMPLETE-UNFILTERED-RETAINED',
  'cryptographic_evidence':'UNAVAILABLE',
  'argument_validation_implementation':'UNFINISHED',
  'production_acceptance_integration':'UNFINISHED',
  'discharged_obligations':[], 'profile_admitted':False}

if __name__=='__main__':
 report=construct()
 (O/'verification/relation-obligations.json').write_text(json.dumps(report,sort_keys=True,indent=2)+'\n')
 print('PASS — relation-aware branches constructed; complete graph retained; zero claims silently discharged.')
