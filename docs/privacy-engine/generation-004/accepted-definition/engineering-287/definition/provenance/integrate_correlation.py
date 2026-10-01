from pathlib import Path
import csv,json,hashlib,shutil,io,re
B=Path('PE-G4-successor-candidate');O=Path('PE-G4-correlation-update');shutil.copytree(B,O,dirs_exist_ok=True)
def sha(b):return hashlib.sha256(b).hexdigest()
def wr(p,s):
 q=O/p;q.parent.mkdir(parents=True,exist_ok=True);q.write_text(s.rstrip()+'\n')
def js(p,v):wr(p,json.dumps(v,indent=2,ensure_ascii=False))
def rows(p):return list(csv.DictReader(p.open(),delimiter='\t'))
def tb(p,rs):
 f=io.StringIO();w=csv.DictWriter(f,list(rs[0]),delimiter='\t',lineterminator='\n');w.writeheader();w.writerows(rs);wr(p,f.getvalue())
P=O/'profile/fragments';fields=rows(P/'fields.tsv');defs=rows(P/'definitions.tsv');ops=rows(P/'operations.tsv');entry=json.loads((P/'entry.json').read_text())
assert len(fields)==118 and len(defs)==56 and len(ops)==89 and entry['groups']==[]
for name in ['DECISION.md','expected-result.json','check_privacy_boundary.py','diagnostic-input.json','proposed_correlation.py','source-excerpts.md']:
 q=O/'evidence/privacy-correction-before-approval'/name;q.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(Path('PE-G4-privacy-diagnostic')/name,q)
wr('privacy/AUTHORIZATION.md','''# Approved unpublished G4 correction

User instruction, 29 September 2026: “Approve observation-aware correlation for unpublished G4. Preserve the complete actor graph, fail unknown visibility, and grant no new public-linkage exceptions. Proceed.”

This selects the proposed correlation assessment boundary for the unpublished candidate. The earlier privacy decision request is satisfied. The root, effect, occurrence, domain and successor construction approvals remain in force. No appointment, evidence signing, admission, publication, succession, deployment, repository edit or registry insertion is authorized or performed.

The integration strengthens the prototype's input contract: a caller-supplied complete flag does not establish visibility, observer coverage or collusion completeness. Every required observation row must resolve under independently authenticated source evidence. Missing or unknown rows fail. Source-trust verification remains an external mandatory stage, never manufactured by this author checker.
''')
ids={r['original_id']:r['candidate_id'] for r in rows(O/'composition/identifier-map.tsv')}
def rename(s):return re.sub(r'E28[34]-DRAFT-[A-Z0-9-]+',lambda m:ids.get(m[0],m[0]),s)
# Exact existing optional producer declarations are included as proposed inputs,
# not promoted to appointed source mechanisms or mandatory policy.
for name in ['dependencies.tsv','evidence-fields.tsv']:
 wr('privacy/producer-proposal/'+name,rename((Path('Engineering-286-producer/producer')/name).read_text()))
wr('privacy/producer-proposal/observer-custody-register.tsv',(Path('Engineering-286-producer/privacy/observer-custody-register.tsv')).read_text())
core=json.loads(Path('PE-G4-privacy-diagnostic/diagnostic-input.json').read_text())['schemas']
N={};E=set();syntax=[]
def node(n,kind,owner,anchor,exposure='CONFIDENTIAL',reuse='NONE',data=''):
 assert n not in N,n;N[n]={'node_id':n,'kind':kind,'owner_source_id':owner,'owner_anchor':anchor,'declared_exposure':exposure,'reuse':reuse,'source_data':data}
def edge(a,b,k):
 assert a in N and b in N,(a,b)
 if a!=b:E.add((a,b,k))
constants=set(json.loads(Path('PE-G4-privacy-diagnostic/diagnostic-input.json').read_text())['constant_fields'])
for schema,fs in core.items():
 owner='PE-G4-SOURCE-'+('S71' if schema in ('AUTHORIZATION-HEADER','COMPONENT-BINDING') else 'S70' if schema.startswith('COMPONENT-0') else 'S72')
 for f in fs:node('CORE:'+schema+'.'+f,'OWNING-SCHEMA',owner,'privacy-schema-'+schema.lower(),reuse='GENERATION-CONSTANT' if f in constants else 'NONE')
for f in fields:
 n='FIELD:'+f['field_id'];node(n,'PROGRAM-FIELD',f['source_id'],f['source_anchor'],data=f['type_id'])
 for part in ['object_id','source','anchor','evidence_id','evidence','endpoint','authoritative','valid','authenticated']:
  m='READ-META:'+f['field_id']+':'+part;node(m,'READ-OBJECT-METADATA',f['source_id'],f['source_anchor']);edge(m,n,'AUTHENTICATES' if part in ('evidence','authenticated','source') else 'REFERENCES')
for o in ops:node('OP:'+o['operation_id'],'DECLARED-OPERATION',o['owner_source_id'],o['owner_anchor'],data=o['expression_owner_id'])
for o in ops:
 for f in o['permitted_read_field_ids'].split(','):
  if f!='NONE':edge('FIELD:'+f,'OP:'+o['operation_id'],'READS')
 for c in o['permitted_call_operation_ids'].split(','):
  if c!='NONE':edge('OP:'+c,'OP:'+o['operation_id'],'CALLS')
def parse(s):
 ts=re.findall(r'[A-Za-z0-9._:#-]+|[(),]',s);assert ''.join(ts)==s;pos=0
 def item():
  nonlocal pos
  name=ts[pos];pos+=1
  if pos==len(ts) or ts[pos]!='(':return name
  pos+=1;args=[]
  while ts[pos]!=')':
   args.append(item())
   if ts[pos]!=',':break
   pos+=1
  assert ts[pos]==')';pos+=1;return (name,args)
 v=item();assert pos==len(ts);return v
for d in defs:
 node('DEF:'+d['definition_id'],'DEFINITION-RESULT',d['source_id'],d['source_anchor'],data=d['output_type_id'])
 for i,t in enumerate([] if d['input_type_ids']=='NONE' else d['input_type_ids'].split(','),1):node('ARG:'+d['definition_id']+f':{i:04}','DEFINITION-PARAMETER',d['source_id'],d['source_anchor'],data=t)
comps={r['component_id']:r['component_order'] for r in rows(P/'candidate-components.tsv')}
def walk(d,tree,path='0001'):
 op,args=tree;n='AST:'+d['definition_id']+':'+path;node(n,'EXPRESSION-'+op.upper(),d['source_id'],d['source_anchor'],data=json.dumps([a for a in args if isinstance(a,str)],separators=(',',':')))
 syntax.append({'definition_id':d['definition_id'],'path':path,'operator':op,'terminal_arguments':N[n]['source_data']})
 children=[]
 for i,a in enumerate(args,1):
  if isinstance(a,tuple):
   child=walk(d,a,path+f'.{i:04}');children.append((i,child));edge(child,n,'DERIVES')
 if op=='arg':edge('ARG:'+d['definition_id']+':'+args[0],n,'REFERENCES')
 if op in ('ref','authoritative','available','valid','authenticated'):
  part='VALUE' if op=='ref' else 'STATUS-'+op.upper();field='PE-TSE-FIELD-COMPONENT-'+comps[args[0]]+'-'+args[1]+'-'+part;edge('FIELD:'+field,n,'REFERENCES')
 if op=='apply' and args[0]!='PE-TSE-SET':
  for i,child in children:edge(child,'ARG:'+args[0]+f':{i-1:04}','ARGUMENT')
  edge('DEF:'+args[0],n,'DERIVES')
 if op=='member':edge('DEF:'+args[1],n,'REFERENCES')
 if op in ('and','or'):
  for i,(_,a) in enumerate(children):
   for _,b in children[i+1:]:edge(a,b,'CONTROLS')
 return n
for d in defs:
 n=walk(d,parse(d['expression']));edge(n,'DEF:'+d['definition_id'],'DERIVES');edge('DEF:'+d['definition_id'],'OP:PE-TSE-OP-DEFINITION-'+d['definition_order'],'DERIVES')
for i,f in enumerate(entry['root_fields'],1):edge('FIELD:'+f,'ARG:'+entry['root_definition']+f':{i:04}','ARGUMENT')
for name,fid in [('n','PE-G4-CAP-READ-NULLIFIER'),('a','PE-G4-CAP-READ-ACTION-CONTEXT'),('r','PE-G4-CAP-READ-DECLARED-ROOT')]:
 node('PUBLIC-PI:'+name,'EXISTING-PUBLIC-INPUT','PE-G4-SOURCE-S76','action-type','PUBLIC',data='PE-TSE-UINT');edge('FIELD:'+fid,'PUBLIC-PI:'+name,'EQUALS');edge('FIELD:PE-G4-CAP-READ-DECLARED-PI','PUBLIC-PI:'+name,'ENCODES')
for a,b in [('n','a'),('a','r'),('n','r')]:edge('PUBLIC-PI:'+a,'PUBLIC-PI:'+b,'OBSERVABLY-JOINABLE')
# Preserve inherited core relationships; no copied count-based all-to-all graph.
from itertools import combinations
aliases={}
for schema,fs in core.items():
 for f in fs:aliases.setdefault(f.replace('-','_'),[]).append('CORE:'+schema+'.'+f)
for f,ns in aliases.items():
 if f.endswith('_id'):
  for a,b in combinations(ns,2):edge(a,b,'REFERENCES')
for i in (1,2):
 prefix=f'CORE:COMPONENT-{i:04}.';edge(prefix+'represented_value',prefix+'canonical_value','DERIVES');edge(prefix+'canonical_value','CORE:COMPONENT-BINDING.bound_value','ENCODES')
 for side in ('AUTHORIZED','CURRENT'):
  for part,name in [('VALUE','canonical_value'),('REPRESENTATION','represented_value')]:edge(f'FIELD:PE-TSE-FIELD-COMPONENT-{i:04}-{side}-{part}',prefix+name,'REPRESENTS')
for f in core['AUTHORIZATION-HEADER']:edge('CORE:AUTHORIZATION-HEADER.'+f,'CORE:COMPONENT-BINDING.authorization_context_digest','DERIVES')
edge('CORE:COMPONENT-BINDING.authorization_context_digest','CORE:COMPONENT-BINDING.bound_value','ENCODES')
for f in ('result','failure_code'):
 edge('CORE:COMPARISON-ATTEMPT.'+f,'CORE:COMPARISON-RESULT.'+f,'REFERENCES');edge('CORE:COMPARISON-RESULT.'+f,'CORE:OBSERVABILITY-OUTPUT.classification','DERIVES')
producer=rows(O/'privacy/producer-proposal/dependencies.tsv');evidence=rows(O/'privacy/producer-proposal/evidence-fields.tsv')
for r in producer:node('PRODUCER:'+r['work_id'],'PROPOSED-PRODUCER-WORK','PE-G4-SOURCE-S83','producer-boundary',data=r['mechanism'])
unresolved=[]
def fieldtarget(f):
 if 'FIELD:'+f in N:return 'FIELD:'+f
 n='UNRESOLVED-PRODUCER-TARGET:'+sha(f.encode())[:16]
 if n not in N:
  node(n,'UNRESOLVED-PRODUCER-TARGET','PE-G4-SOURCE-S83','producer-boundary',data=f);unresolved.append({'work_id':'UNRESOLVED-TARGET','condition_node':n,'exact_condition':f,'status':'Prose target is not a canonical field identity'})
 return n
for r in producer:
 for j,p in enumerate(r['predecessors'].split(';'),1):
  p=p.strip()
  if p=='NONE':continue
  if 'PRODUCER:'+p in N:edge('PRODUCER:'+p,'PRODUCER:'+r['work_id'],'CONTROLS')
  else:
   z='PRODUCER-CONDITION:'+r['work_id']+f':{j:04}';node(z,'UNRESOLVED-PRODUCER-CONDITION','PE-G4-SOURCE-S83','producer-boundary',data=p);edge(z,'PRODUCER:'+r['work_id'],'REQUIRES-SOURCE-RESOLUTION');unresolved.append({'work_id':r['work_id'],'condition_node':z,'exact_condition':p,'status':'Not silently translated into an executable dependency'})
 for f in r['retained_field_ids'].split(';'):
  if f!='NONE':edge('PRODUCER:'+r['work_id'],fieldtarget(f),'PROPOSED-PRODUCES')
for r in evidence:
 n='PRODUCER-EVIDENCE:'+r['record']+':'+r['field'];node(n,'PROPOSED-EVIDENCE-FIELD','PE-G4-SOURCE-S83','producer-boundary',data=r['encoding'])
 for f in r['consumer_fields'].split(';'):
  if f!='NONE':edge(n,fieldtarget(f),'PROPOSED-SUPPORTS')
 for p in producer:
  if p['evidence_record']==r['record']:edge('PRODUCER:'+p['work_id'],n,'PROPOSED-PRODUCES')
tb('privacy/model/unresolved-producer-conditions.tsv',unresolved)
tb('privacy/model/nodes.tsv',list(N.values()));tb('privacy/model/structural-edges.tsv',[{'from_node':a,'to_node':b,'relation':k} for a,b,k in sorted(E)]);tb('privacy/model/expression-syntax.tsv',syntax)
tb('privacy/model/field-coverage.tsv',[{'field_id':f['field_id'],'surface_node':'FIELD:'+f['field_id'],'metadata_count':'9','root_argument_order':str(entry['root_fields'].index(f['field_id'])+1) if f['field_id'] in entry['root_fields'] else 'NOT-APPLICABLE'} for f in fields])
js('privacy/model/construction.json',{'format':'PE-G4-OBSERVATION-MODEL-CANDIDATE-V1','contexts':['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'],'node_templates':len(N),'structural_edge_templates':len(E),'program_fields':len(fields),'root_inputs':len(entry['root_fields']),'operations':len(ops),'definitions':len(defs),'producer_work_rows':len(producer),'producer_evidence_fields':len(evidence),'core_public_output_selected':False,'existing_public_pi':['n','a','r'],'actor_graph':'ALL generated edges; no visibility or constant-edge filtering','equality_expansion':'Retain governing conservative two-context potential-equality generation; no new permitted equality classes. Instantiate in the full graph before actor assessment. The stored structural template is not that expanded occurrence/admission graph.','source_completeness':'UNESTABLISHED: producer declarations remain proposed; extra live observer/custody/metadata paths require source closure.','actual_visibility_evidence':None,'threat_model_appointment':None,'canonical_outer_profile':None,'profile_admitted':False})
wr('privacy/model/README.md','''# Regenerated declared-surface model

Every declared program field now has a dedicated surface, including all 94 root inputs and all 24 AUTHORIZED/CURRENT component fields. Nine non-value ReadObject metadata cells are represented per field; the field surface represents value. All declared operations, parameters, every AST branch and call argument are present. No issuer chooses a subset of these edges. The existing public PI values n,a,r and their aliases are explicit PUBLIC surfaces; no new public U/classification output has been selected by this construction.

The thirty-two proposed producer work rows and 174 proposed evidence fields are represented explicitly as proposed surfaces/edges. They do not establish source competence or a complete deployed observer universe. In particular they do not promote a shared serialization mechanism or initial FALSE map into protocol policy. Their exact source adequacy remains unclosed. Entry groups are empty in the supplied program; this construction asserts that fact, not a rule forbidding future groups.

This is a deterministic static declaration model, not an admitted privacy object or runtime transcript. Context-sensitive repeated READ/invocation identities and actual evidence remain governed by exact replay. The two-context symbolic equality expansion remains an explicit generator obligation; structural-edges.tsv alone is not the complete actor graph. The assessor must receive the full regenerated graph, and its actor check uses every supplied regenerated edge. No actor-safety claim follows from there being no actual actor-bearing input in this documentary inventory.

No visibility matrix is fabricated. Source-grounded observer scope and coalition completeness are external admission inputs. Missing entries become UNKNOWN, and unknown visibility fails. Core schemas and component abstractions remain present alongside detailed fields, rather than being used to erase them. The full model must be canonically bound in the revised privacy member before full profile serialization/admission; this candidate does not claim that integration is complete.
''')
wr('privacy/KNOWN-PUBLIC-ROOT-BOUNDARY.md','''# Remaining boundary under the approved no-exceptions rule

Public r remains a public proof input. Two different action occurrences can legitimately use the same eligible root: the selected policy does not consume a root, require root uniqueness per action, or require a new introduction between actions. This is true even when a and n differ. No actual occurrence is asserted here.

With both root values visible to the public observer, their equality is an observable cross-context edge. r has no authorized GENERATION-CONSTANT reuse class: roots change, and this approval expressly grants no new public-linkage exceptions. Therefore the approved observation-aware criterion still returns CORRELATION-FAILURE for that valid shared-root author vector. Hiding private internal paths cannot remove a directly observable public equality.

This is a remaining source-policy boundary, not an absent appointment or a failure of source authentication. This integration neither suppresses public r, relabels it as a constant, changes occurrence identity, weakens actor tests nor authorizes an exception. It does not claim that the approved correction alone makes the selected capability admissible. The exact construction remains available for further source determination; no new approval is silently inferred.
''')
print(json.dumps({'nodes':len(N),'edges':len(E),'syntax_nodes':len(syntax),'producer':len(producer),'evidence':len(evidence)}))
