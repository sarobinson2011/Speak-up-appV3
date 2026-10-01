"""Regenerate declared model from packaged inputs; compare every generated row.
No historical code is executed and no files are written by this checker.
"""
from pathlib import Path
import csv,json,re,hashlib
O=Path(__file__).resolve().parents[1]
def rows(p):return list(csv.DictReader(p.open(),delimiter='\t'))
def sha(b):return hashlib.sha256(b).hexdigest()
P=O/'profile/fragments';fields=rows(P/'fields.tsv');defs=rows(P/'definitions.tsv');ops=rows(P/'operations.tsv');entry=json.loads((P/'entry.json').read_text())
assert entry['groups']==[], 'A nonempty group declaration requires explicit canonical group construction.'
core=json.loads((O/'evidence/privacy-correction-before-approval/diagnostic-input.json').read_text())['schemas']
N={};E=set();syntax=[]
def node(n,kind,owner,anchor,exposure='CONFIDENTIAL',reuse='NONE',data=''):
 assert n not in N,n;N[n]={'node_id':n,'kind':kind,'owner_source_id':owner,'owner_anchor':anchor,'declared_exposure':exposure,'reuse':reuse,'source_data':data}
def edge(a,b,k):
 assert a in N and b in N,(a,b)
 if a!=b:E.add((a,b,k))
constants=set(json.loads((O/'evidence/privacy-correction-before-approval/diagnostic-input.json').read_text())['constant_fields'])
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

# S84's source-bound role metadata is part of the full declared graph.
for role in ('n','a','r'):
 for field in ('role','owner_source_id','source_sha256','source_anchor','scope_id','value_hex','action_node'):
  n='PUBLIC-ROLE-BINDING:'+role+':'+field
  node(n,'PUBLIC-RELATIONSHIP-EVIDENCE','PE-G4-SOURCE-S84','binding-schema',data=field)
  edge(n,'PUBLIC-PI:'+role,'ROLE-BINDING')
edge('PUBLIC-ROLE-BINDING:n:action_node','PUBLIC-PI:a','REFERENCES')

expected={
 'nodes.tsv':list(N.values()),
 'structural-edges.tsv':[{'from_node':a,'to_node':b,'relation':k} for a,b,k in sorted(E)],
 'expression-syntax.tsv':syntax,
 'unresolved-producer-conditions.tsv':unresolved,
 'field-coverage.tsv':[{'field_id':f['field_id'],'surface_node':'FIELD:'+f['field_id'],'metadata_count':'9','root_argument_order':str(entry['root_fields'].index(f['field_id'])+1) if f['field_id'] in entry['root_fields'] else 'NOT-APPLICABLE'} for f in fields],
}
for name,generated in expected.items():
 assert rows(O/'privacy/model'/name)==generated, 'Canonical model mismatch: '+name
print('PASS — every declared model row independently regenerated from packaged inputs.')
