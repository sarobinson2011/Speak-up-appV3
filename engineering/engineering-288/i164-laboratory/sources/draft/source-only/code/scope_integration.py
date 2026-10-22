"""Mandatory SOURCE-ONLY entry point composing existing candidate/procedure APIs.
No deployment, operational attestation, new allowance or canonical registration.
"""
import argparse,copy,hashlib,json,sys
from pathlib import Path
P=Path(__file__).resolve().parents[1]
PINS=(('scope','10484a479188867ed6011dd07679cbd816be412dbb6570c6e93988bbdd23a8fb'),('universe','e71fa0d5906477032f128eeb0247715eed3daaa063a8af43a5f4c5c27d55b2de'))
FORMAT='I164-SOURCE-ONLY-CANDIDATE-VALIDATION-1'
def need(b,s):
 if not b:raise ValueError(s)
def enc(v):return json.dumps(v,sort_keys=True,separators=(',',':'),ensure_ascii=False,allow_nan=False).encode()
def sha(b):return hashlib.sha256(b).hexdigest()
def identity(p):
 b=Path(p).read_bytes();return {'bytes':len(b),'sha256':sha(b)}
def load(p):
 def pairs(xs):
  d={}
  for k,v in xs:need(k not in d,'DUPLICATE-JSON-KEY');d[k]=v
  return d
 return json.loads(Path(p).read_bytes(),object_pairs_hook=pairs,parse_constant=lambda v:(_ for _ in ()).throw(ValueError('NONFINITE-JSON')))
def same(a,b,s):need(enc(a)==enc(b),s)
def verified_inputs():
 # Expectations come from immutable versioned authority input identities, reread
 # on every call, never a returned mutable dictionary or caller-supplied pin map.
 for name,pin in PINS:
  base=P/name;need(identity(base/'MANIFEST.json')['sha256']==pin,'INPUT-MANIFEST:'+name);m=load(base/'MANIFEST.json')
  files={str(q.relative_to(base)) for q in base.rglob('*') if q.is_file()}
  need(files==set(m)|{'MANIFEST.json'},'INPUT-MEMBERSHIP:'+name)
  for n,v in m.items():
   q=base/n;need(not q.is_symlink() and q.resolve().is_relative_to(base.resolve()),'INPUT-PATH');same(identity(q),v,'INPUT-BYTES:'+n)
 return {'scope':load(P/'scope/protected-scope-v2.json'),'expressions':load(P/'scope/expression-bindings.json'),'obligations':load(P/'scope/remaining-obligations.json')}
def preflight(root,submitted=None):
 expected=verified_inputs()
 if submitted is not None:same(submitted,expected,'SCOPE-SUBSTITUTION')
 sys.path.insert(0,str(P/'universe/code'));import universe as u
 root,_=u.c.verify_root(root)
 x=load(P/'universe/outputs/universe.json');s=expected['scope'];e=expected['expressions'];o=expected['obligations']
 need(s['assessment_target']['designation']=='SOURCE-ONLY' and s['assessment_target']['installation_designated'] is False and s['assessment_target']['operator_designated'] is False,'SOURCE-ONLY')
 same(s['candidate_binding'],x['candidate_binding'],'CANDIDATE-BINDING')
 same(e['scope_manifest_identity'],identity(P/'scope/protected-scope-v2.json'),'SCOPE-IDENTITY')
 same(o['scope_manifest_identity'],e['scope_manifest_identity'],'OBLIGATION-BINDING')
 same(e['current_universe_identity'],identity(P/'universe/outputs/universe.json'),'UNIVERSE-BINDING')
 same(e['native_consumption_identity'],identity(P/'universe/outputs/consumption.json'),'CONSUMPTION-BINDING')
 for source in s['sources'].values():same(identity(root/source['path']),{k:source[k] for k in ('bytes','sha256')},'CURRENT-SOURCE')
 need(all(v is None for v in s['unknown_operational_sets'].values()),'UNKNOWN-DOMAINS')
 need(s['global_lifetime_bound'] is None and s['global_storage_byte_bound'] is None,'UNKNOWN-BOUNDS')
 same([f['family'] for f in e['families']],[f['family'] for f in x['families']],'FAMILY-COVERAGE')
 for a,b in zip(e['families'],x['families']):
  same(a['expression'],b['count_expression'],'COUNT-EXPRESSION');same(a['directory_ids'],b['directory_ids'],'DIRECTORY-COVERAGE');need(a['domain_value'] is None,'UNKNOWN-DOMAIN')
 same([a['scope_id'] for a in s['protected_logical_scope']],[a['id'] for a in x['protected_carriers']],'CARRIER-COVERAGE')
 same(s['existing_context_associations'],load(root/'candidate/contexts.json'),'CONTEXT-BINDING')
 return root,expected,x

def validate(root,submitted=None):
 root,b,x=preflight(root,submitted)
 import universe as u
 used=u.consume(root,x) # authoritative directory/count-only/procedure derivation
 import layout_consumers as lc
 from semantic import setup
 import prospective_procedure as procedure
 values={k:load(root/v) for k,v in lc.PATHS.items()}
 same(sha(enc(values['procedure'])),used['existing_procedure_sha256'],'PROCEDURE-CURRENT')
 c=setup(root);same(c.binding,b['scope']['candidate_binding'],'CURRENT-CANDIDATE')
 rows=[]
 for context in ('SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'):
  # Small unchanged saved export, not a new runtime execution. Both contexts
  # are exercised; no whole-program or full signing lifecycle coverage claim.
  path='support/fixtures/minimal-response.json';export=load(root/path)
  occ=c.ingest(export,context,c.binding)
  duty=procedure.consume(values['procedure'],values['directory'],values['rules'],occ,export)
  rows.append({'context':context,'evidence':{'path':path,**identity(root/path),'kind':'RETAINED-SAVED-EXPORT; no producer rerun'},'candidate_occurrence_sha256':sha(enc(occ)),'response_associations':len(occ['response_associations']),'mechanical_duty_result':duty,'candidate_blockers':occ['blockers']})
 return copy.deepcopy({'format':FORMAT,'scope':'SOURCE-ONLY; bounded candidate correspondence only','scope_input_identity':identity(P/'scope/protected-scope-v2.json'),'expression_input_identity':identity(P/'scope/expression-bindings.json'),'obligation_input_identity':identity(P/'scope/remaining-obligations.json'),'integration_source':identity(Path(__file__)),'candidate_binding':c.binding,'contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'consumption':used,'observations':rows,'obligations':b['obligations']['obligations'],'unknown_operational_sets':b['scope']['unknown_operational_sets'],'entry_points':['universe.consume','cardinality.consume','layout_consumers.derive','Candidate.ingest','prospective_procedure.consume'],'operational_assurance':False,'global_lifetime_bound':None,'global_storage_byte_bound':None,'canonical_registration':False,'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED','backup':'KERNEL-ONLY'})
def validate_result(root,result,submitted=None):
 _,b,_=preflight(root,submitted)
 need(type(result) is dict and result.get('format')==FORMAT,'PARTIAL-OR-LEGACY-RESULT')
 for key,v in {'operational_assurance':False,'global_lifetime_bound':None,'global_storage_byte_bound':None,'canonical_registration':False,'full_expansion_ready':False,'final_binding':'BLOCKED','actual_admission':False,'stream_identities':'UNCOMPUTED','backup':'KERNEL-ONLY'}.items():
  need(key in result,'MISSING-RESULT-FIELD');same(result[key],v,'RESULT-ESCALATION:'+key)
 same(result.get('obligations'),b['obligations']['obligations'],'RESULT-OBLIGATIONS')
 same(result.get('unknown_operational_sets'),b['scope']['unknown_operational_sets'],'RESULT-UNKNOWNS')
 same(result.get('contexts'),[v['context'] for v in b['scope']['existing_context_associations']['associations']],'RESULT-CONTEXTS')
 same(result,validate(root,submitted),'RESULT-SUBSTITUTION');return True
if __name__=='__main__':
 ap=argparse.ArgumentParser();ap.add_argument('--root',required=True);ap.add_argument('--output');ap.add_argument('--result');a=ap.parse_args()
 if a.result:validate_result(a.root,load(a.result));print('PASS SOURCE-ONLY current-result correspondence; readiness BLOCKED')
 else:
  need(a.output,'OUTPUT-REQUIRED');dest=Path(a.output);need(not dest.exists(),'OUTPUT-EXISTS');v=validate(a.root);dest.write_bytes(enc(v));print('PASS SOURCE-ONLY candidate/directory/procedure integration; no operational assurance')
