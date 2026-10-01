"""Fresh, read-only diagnostic of supplied declaration data. No old source code executes."""
from pathlib import Path
import json,hashlib,collections
P=Path(__file__).resolve().parent
D=json.loads((P/'diagnostic-input.json').read_text())
H=lambda b:hashlib.sha256(b).hexdigest()

def model(public_output):
 surfaces=[]
 for schema,fields in D['schemas'].items():
  for name in fields:
   exposure='PUBLIC' if schema=='OBSERVABILITY-OUTPUT' and public_output else 'CONFIDENTIAL'
   reuse='NONE';domain='OPAQUE'
   if name.replace('-','_')=='transition_occurrence_id':domain='ACTION-IDENTITY'
   if name in D['constant_fields']:reuse='GENERATION-CONSTANT';domain='CONSTANT:'+schema+'.'+name
   surfaces.append(dict(schema=schema,field=name,exposure=exposure,reuse=reuse,domain=domain))
 tokens=[]
 for context in ('U-ONE','U-TWO'):
  for s in surfaces:
   for record in range(1,3 if s['schema']=='COMPONENT-BINDING' else 2):
    value=('FRESH:'+context if s['domain']=='ACTION-IDENTITY' else 'CONSTANT:'+s['domain'] if s['reuse']!='NONE' else 'ARBITRARY').encode()
    tokens.append(dict(s,context=context,record=record,digest=H(value),id=f'T{len(tokens)+1:04}'))
 # Exact equality branch of S70 universe. Structural relations are not needed
 # for a failure witness: adding those edges cannot eliminate this path.
 edges=[]
 for i,x in enumerate(tokens):
  for y in tokens[i+1:]:
   arbitrary=lambda t:t['domain']!='ACTION-IDENTITY' and t['reuse']=='NONE'
   if x['digest']==y['digest'] or arbitrary(x) or arbitrary(y):
    permitted=x['reuse']==y['reuse'] and x['reuse']!='NONE'
    edges.append((x['id'],y['id'],permitted))
 byid={t['id']:t for t in tokens};graph={t['id']:[] for t in tokens}
 for a,b,permitted in edges:
  if not permitted:graph[a].append(b);graph[b].append(a)
 publics=[t for t in tokens if t['exposure']=='PUBLIC'];witness=None
 for start in publics:
  parents={start['id']:None};queue=collections.deque([start['id']])
  while queue and witness is None:
   here=queue.popleft();t=byid[here]
   if t['exposure']=='PUBLIC' and t['context']!=start['context']:
    path=[]
    while here is not None:path.append(byid[here]);here=parents[here]
    witness=list(reversed(path));break
   for nxt in sorted(graph[here]):
    if nxt not in parents:parents[nxt]=here;queue.append(nxt)
  if witness is not None:break
 return {'public_output':public_output,'surface_count':len(surfaces),'token_count':len(tokens),'public_token_count':len(publics),'equality_edge_count':len(edges),'correlation_failure_witness':witness,'correlation_full_model_result':'FAIL-PROVEN-BY-SUBGRAPH' if witness else 'NOT-ASSESSED' if publics else 'NO-PUBLIC-ENDPOINTS-IN-THIS-MODEL','actor_test':'NOT-EVALUATED; no actor-risk clearance inferred'}

private=model(False);public=model(True)
assert private['public_token_count']==0
assert public['correlation_failure_witness'] is not None
w=public['correlation_failure_witness'];assert w[0]['context']!=w[-1]['context'] and w[0]['exposure']==w[-1]['exposure']=='PUBLIC'
assert any(t['exposure']=='CONFIDENTIAL' for t in w[1:-1])
# Canonical schemas lack a field-specific surface for any of the 94 E inputs.
root_fields=set(D['root_fields']);schemafields={s+'.'+f for s,fs in D['schemas'].items() for f in fs}
assert len(root_fields)==94 and not root_fields & schemafields
result={'diagnostic_checks':'PASS','meaning':'The source-model obstruction is reproduced, not repaired; this is not a privacy admission result.','exact_program_fields':len(D['fields']),'root_inputs_without_dedicated_schema_surface':94,'component_program_fields':len(D['fields'])-94,'private_output_case':private,'public_output_case':public,'fixed_source_sha256':D['source_sha256'],'historical_code_executed':False,'source_or_privacy_appointment_created':False}
expected=json.loads((P/'expected-result.json').read_text())
assert result==expected,'Diagnostic differs from the supplied expected result.'
print('PASS — privacy-construction obstruction reproduced from fixed declarations.')
print('94 Evaluation input fields have no dedicated surface in the inherited canonical model.')
print('Public output enabled: CORRELATION-FAILURE follows from the retained equality rule.')
print('Public output disabled: the model has no public endpoints; this does not cover public PI.')
print('Repository unchanged. No profile admission, publication or historical code execution.')
