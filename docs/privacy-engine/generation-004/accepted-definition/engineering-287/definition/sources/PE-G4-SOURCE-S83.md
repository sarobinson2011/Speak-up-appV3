# PE-G4-SOURCE-S83 — approved observation-aware correlation construction

Status: unpublished G4 source candidate; user-authorized construction, not independently appointed or admitted. The precise user approval is preserved in privacy/AUTHORIZATION.md.

This source specializes the G4 interpretation of retained S70/S71/S72 privacy construction, specifically full declared-surface regeneration and the correlation graph criterion. Historical G3 sources remain byte-exact. This is an explicit approved procedural delta, not a silent correction of published G3. Every other governing validation, source/evidence appointment, evidence authentication, full actor graph, uniqueness duty and ordered failure precedence remains binding.

<a id="universe"></a>
## universe

The G4 privacy construction MUST include every declared program field, root argument, component side/status, ReadObject metadata cell, operation, expression branch, parameter/call/control relationship, governing owning schema, public PI alias and source-required producer observation/custody path; absent source completeness MUST remain an admission failure.

<a id="visibility"></a>
## visibility

Every required observer and coalition visibility assessment MUST be independently source-established for the exact regenerated graph; missing or unknown visibility MUST fail, and a caller-supplied completeness flag MUST NOT substitute for that evidence.

<a id="correlation"></a>
## correlation

Cross-context correlation assessment MUST use the independently established observable graph for each required observer coalition, preserve the existing permitted constant-equality exception only in that assessment, and include equality of values visible to that coalition.

<a id="actor"></a>
## actor

Actor-reconstruction assessment MUST retain the complete regenerated graph, including confidential, non-observed and permitted constant-equality edges, without visibility filtering.

<a id="no-exceptions"></a>
## no-exceptions

The observation-aware correction MUST NOT introduce public-linkage exceptions, suppress existing public PI, convert changing roots or action-local values into generation constants, or waive the unchanged public uniqueness and actor-protection obligations.

<a id="producer-boundary"></a>
## Producer and completeness boundary

The graph templates preserve all supplied program declarations and proposed producer surfaces. Prose producer predecessors/targets without exact operation/field identities are explicit UNRESOLVED nodes; they do not become fabricated executable links. Shared serialization and total-map FALSE examples remain optional unappointed mechanisms, not new protocol policy. Unknown actual provider, custody, observer and collusion facts remain missing evidence. No source-truth or completeness claim is established by this authoring model.

<a id="procedure"></a>
## Exact graph procedure and staged integration

privacy/observation_correlation.py below supplies the exact graph subroutine and twelve synthetic author vectors. It requires the complete independently regenerated graph, including the unchanged conservative equality expansion, and externally authenticated required observer/coalition scope and visibility cells. The graph subroutine does not perform those external validations and never returns a profile admission PASS. Its complete per-view cell domain rejects missing entries. Coalition views cannot erase observations of their members. Visible value equality cannot be hidden by an issuer's edge label. Negative visibility requires source evidence; confidentiality labels do not prove non-observation.

Actor reconstruction uses every graph edge even when visibility is invalid. Uniqueness retains its original public-byte equality condition. Failures are collected in the inherited ordered list; e.g. shared public root equality produces UNIQUENESS-FAILURE before CORRELATION-FAILURE. No earlier authentication failure is bypassed in the full governing pipeline.

The declaration model includes every supplied 118-field program input and metadata cell, all AST branches, owning schemas, operations and the optional producer inventory. It remains a static construction template, not a full runtime graph. Source-complete observer/custody declarations, conservative two-context equality expansion, repeated occurrence/replay bindings, canonical binding of the expanded privacy member and integrated evidence validation remain mandatory before outer-profile admission. None is inferred from graph-vector success. Source adequacy of the producer proposal and remaining coordinates/material conditions stays open.

The construction's new declaration inputs and output templates are digest-bound by privacy/model/manifest.json. Until the complete model/evidence is canonically incorporated into the governing PRIVACY member, no final full-profile digest exists. No ad hoc extra graph attached to the old immutable container can substitute for that incorporation.

The following executable notation is newly authored G4 construction code. Its source-validation prerequisites are normative; fixture test inputs have no source authority. No historical constructor has been executed.

```python
"""G4 candidate graph procedure; not an admission/signature/source validator.

Call only after independent regeneration of the COMPLETE graph (including the
conservative equality expansion) and authentication of exact observer/threat and
visibility evidence. This module cannot establish those external facts. Tests
supply synthetic author vectors. No labels or caller 'complete' flags prove
source coverage. There is no overall profile PASS returned here.
"""
from itertools import combinations
import hashlib,json
ORDER=['INVALID-PROFILE-SCHEMA','PROFILE-DIGEST-MISMATCH','INVALID-EVIDENCE-AUTHORITY','MISSING-EVIDENCE','INVALID-EVIDENCE-AUTHENTICATION','INVALID-EVIDENCE-DIGEST','INVALID-SURFACE-LABELS','INVALID-ACTION-CONTEXT','INCOMPLETE-EVIDENCE-UNIVERSE','COMPONENT-COUNT-MISMATCH','UNNECESSARY-COMPONENT','PUBLIC-PRIVATE-VALUE','REUSABLE-IDENTIFIER','OPENING-DISCLOSURE','UNIQUENESS-FAILURE','CORRELATION-FAILURE','ACTOR-RECONSTRUCTION-RISK','COMPONENT-FAILURE']
STATES={'VISIBLE','HIDDEN','UNKNOWN'}
def digest(value):return hashlib.sha256(value.encode()).hexdigest()
def graph_checks(nodes,edges,required_views,visibility):
    """nodes: id -> context/exposure/reuse/digest.
    edges: distinct (from,to,relation) triples, ALL regenerated actor edges.
    required_views: exact externally established tuple of observer coalitions.
    visibility: coalition -> {'nodes': id->state, 'edges': index->state}.
    All singleton observers must occur. Missing/unknown cells fail. Complete
    required_views and negative HIDDEN assertions need source evidence outside
    this graph subroutine; callers may not select a convenient threat model.
    """
    failures=set()
    def result():return {'scope':'GRAPH-CHECKS-ONLY-NOT-PROFILE-ADMISSION','failures':[x for x in ORDER if x in failures],'earliest_failure':next((x for x in ORDER if x in failures),'NONE')}
    if not nodes or len(set(edges))!=len(edges) or any(len(e)!=3 or e[0] not in nodes or e[1] not in nodes or e[0]==e[1] for e in edges):
        failures.add('INVALID-PROFILE-SCHEMA');return result()
    if any(set(n)!= {'context','exposure','reuse','digest'} or n['exposure'] not in ('PUBLIC','CONFIDENTIAL','PRIVATE-ACTOR') or n['reuse'] not in ('NONE','GENERATION-CONSTANT') for n in nodes.values()):
        failures.add('INVALID-SURFACE-LABELS');return result()
    if any(not isinstance(n['digest'],str) or len(n['digest'])!=64 or any(c not in '0123456789abcdef' for c in n['digest']) for n in nodes.values()):
        failures.add('INCOMPLETE-EVIDENCE-UNIVERSE');return result()
    public={k for k,v in nodes.items() if v['exposure']=='PUBLIC'};actors={k for k,v in nodes.items() if v['exposure']=='PRIVATE-ACTOR'}
    def reach(start,es):
        adj={n:set() for n in nodes}
        for a,b,k in es:adj[a].add(b);adj[b].add(a)
        seen=set();todo=[start]
        while todo:
            n=todo.pop()
            if n in seen:continue
            seen.add(n);todo.extend(adj[n]-seen)
        return seen
    # Actor reconstruction ALWAYS uses the full graph, even if visibility fails.
    if any(reach(n,edges)&actors for n in public):failures.add('ACTOR-RECONSTRUCTION-RISK')
    # Original uniqueness obligation is unchanged by correlation approval.
    for a,b in combinations(sorted(public),2):
        x,y=nodes[a],nodes[b]
        if x['context']!=y['context'] and x['digest']==y['digest'] and not (x['reuse']==y['reuse']!='NONE'):failures.add('UNIQUENESS-FAILURE')
    if not required_views or any(not isinstance(v,tuple) or not v or tuple(sorted(set(v)))!=v for v in required_views) or len(set(required_views))!=len(required_views):
        failures.add('INCOMPLETE-EVIDENCE-UNIVERSE');return result()
    observers=set().union(*(set(v) for v in required_views))
    if any((o,) not in required_views for o in observers):failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
    if set(visibility)!=set(required_views):failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
    for view in required_views:
        v=visibility.get(view,{});vn=v.get('nodes',{});ve=v.get('edges',{})
        if set(v)!={'nodes','edges'} or set(vn)!=set(nodes) or set(ve)!=set(range(len(edges))):failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
        if any(s not in STATES for s in [*vn.values(),*ve.values()]):failures.add('INVALID-SURFACE-LABELS')
        if any(vn.get(n,'UNKNOWN')=='UNKNOWN' for n in nodes) or any(ve.get(i,'UNKNOWN')=='UNKNOWN' for i in range(len(edges))):failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
        if any(vn.get(n)!='VISIBLE' for n in public):failures.add('INVALID-SURFACE-LABELS')
        # Coalition observations cannot erase their members' observations.
        for member in view:
            one=visibility.get((member,),{})
            if any(s=='VISIBLE' and vn.get(n)!='VISIBLE' for n,s in one.get('nodes',{}).items()):failures.add('INVALID-SURFACE-LABELS')
            if any(s=='VISIBLE' and ve.get(i)!='VISIBLE' for i,s in one.get('edges',{}).items()):failures.add('INVALID-SURFACE-LABELS')
        observed=[]
        for i,(a,b,k) in enumerate(edges):
            both=vn.get(a)==vn.get(b)=='VISIBLE';state=ve.get(i,'UNKNOWN')
            if state=='VISIBLE' and not both:failures.add('INVALID-SURFACE-LABELS')
            # Equality of exposed canonical values is observable; the issuer
            # cannot hide its graph edge merely by withholding an edge label.
            if k=='EQUALS' and both:
                if state!='VISIBLE':failures.add('INVALID-SURFACE-LABELS')
                state='VISIBLE'
            permitted=k=='EQUALS' and nodes[a]['reuse']==nodes[b]['reuse']!='NONE'
            if state=='VISIBLE' and both and not permitted:observed.append((a,b,k))
        for a,b in combinations(sorted(public),2):
            if nodes[a]['context']!=nodes[b]['context'] and b in reach(a,observed):failures.add('CORRELATION-FAILURE')
    return result()

def test_vectors():
    cases=[]
    def n(c,e='PUBLIC',value=None,reuse='NONE'):return {'context':c,'exposure':e,'reuse':reuse,'digest':digest(value or c+':'+e)}
    nodes={'u1':n('ONE'),'u2':n('TWO'),'internal':n('ONE','CONFIDENTIAL')};edges=[('u1','internal','EQUALS'),('internal','u2','EQUALS')]
    def view(ns,es):return {'nodes':{k:'VISIBLE' if k in ns else 'HIDDEN' for k in nodes},'edges':{i:'VISIBLE' if i in es else 'HIDDEN' for i in range(len(edges))}}
    views=[('public',)];v={views[0]:view({'u1','u2'},set())}
    def expect(name,nodes,edges,vs,matrix,expected):
        r=graph_checks(nodes,edges,vs,matrix);assert r['earliest_failure']==expected,(name,r);cases.append({'case':name,**r});return r
    expect('confidential path is not asserted publicly observable',nodes,edges,views,v,'NONE')
    expect('source-established observable path fails',nodes,edges,views,{views[0]:view(set(nodes),{0,1})},'CORRELATION-FAILURE')
    unknown={views[0]:view({'u1','u2'},set())};unknown[views[0]]['nodes']['internal']='UNKNOWN'
    expect('unknown visibility fails',nodes,edges,views,unknown,'INCOMPLETE-EVIDENCE-UNIVERSE')
    incomplete={views[0]:view({'u1','u2'},set())};del incomplete[views[0]]['edges'][1]
    expect('omitted edge visibility fails',nodes,edges,views,incomplete,'INCOMPLETE-EVIDENCE-UNIVERSE')
    expect('absent threat model fails',nodes,edges,[],{},'INCOMPLETE-EVIDENCE-UNIVERSE')
    hidden_public={views[0]:view({'u1'},set())}
    expect('cannot relabel public visibility',nodes,edges,views,hidden_public,'INVALID-SURFACE-LABELS')
    # Full actor graph retained, including hidden edges and constant exception.
    na=dict(nodes,actor=n('ONE','PRIVATE-ACTOR'));ea=edges+[('internal','actor','DERIVES')]
    va={views[0]:{'nodes':{k:'VISIBLE' if k in ('u1','u2') else 'HIDDEN' for k in na},'edges':{i:'HIDDEN' for i in range(3)}}}
    expect('hidden actor bridge still fails',na,ea,views,va,'ACTOR-RECONSTRUCTION-RISK')
    nc={'u1':n('ONE',reuse='GENERATION-CONSTANT'),'actor':n('TWO','PRIVATE-ACTOR',reuse='GENERATION-CONSTANT')};ec=[('u1','actor','EQUALS')]
    vc={views[0]:{'nodes':{'u1':'VISIBLE','actor':'HIDDEN'},'edges':{0:'HIDDEN'}}}
    expect('constant exception never filters actor graph',nc,ec,views,vc,'ACTOR-RECONSTRUCTION-RISK')
    # Direct public PI equality keeps BOTH failure obligations; no exemption.
    nr={'r1':n('ONE',value='canonical-root-7'),'r2':n('TWO',value='canonical-root-7')};er=[('r1','r2','EQUALS')]
    vr={views[0]:{'nodes':{'r1':'VISIBLE','r2':'VISIBLE'},'edges':{0:'VISIBLE'}}}
    r=expect('same public root across distinct contexts',nr,er,views,vr,'UNIQUENESS-FAILURE');assert 'CORRELATION-FAILURE' in r['failures']
    suppressed={views[0]:{'nodes':dict(vr[views[0]]['nodes']),'edges':{0:'HIDDEN'}}}
    r=expect('cannot suppress visible public equality',nr,er,views,suppressed,'INVALID-SURFACE-LABELS');assert 'CORRELATION-FAILURE' in r['failures']
    # Two individually unlinked observers can compose through a shared value.
    ne={'u1':n('ONE'),'u2':n('TWO'),'m':n('ONE','CONFIDENTIAL')};ee=[('u1','m','REFERENCES'),('m','u2','REFERENCES')]
    coal=[('left',),('right',),('left','right')];allnodes={k:'VISIBLE' for k in ne}
    vv={('left',):{'nodes':dict(allnodes),'edges':{0:'VISIBLE',1:'HIDDEN'}},('right',):{'nodes':dict(allnodes),'edges':{0:'HIDDEN',1:'VISIBLE'}},('left','right'):{'nodes':dict(allnodes),'edges':{0:'VISIBLE',1:'VISIBLE'}}}
    expect('coalition path fails',ne,ee,coal,vv,'CORRELATION-FAILURE')
    vv[('left','right')]['edges'][1]='HIDDEN'
    expect('coalition cannot erase member observations',ne,ee,coal,vv,'INVALID-SURFACE-LABELS')
    return cases
if __name__=='__main__':
    cases=test_vectors();print('PASS — '+str(len(cases))+' graph vectors; actor graph and no-exception rules retained.');print('Shared public root: UNIQUENESS-FAILURE and CORRELATION-FAILURE, as required.');print('Graph checks only. No privacy admission or publication performed.')
```

## Exact declaration-template generator

This deterministic generator compares every generated node, structural edge, AST record, field-coverage row and unresolved producer clause against the supplied templates. It rejects a modified cache. This does not establish missing producer/observer source facts or generate a real occurrence.

```python
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
```
