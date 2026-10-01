# PE-G4-SOURCE-S84 — approved bounded public-input relationships

Status: unpublished construction candidate, not appointed or admitted. The exact approval basis is privacy/PUBLIC-RELATIONSHIP-AUTHORIZATION.md. This source specializes S83#no-exceptions only for the three approved public relationships and their corresponding public uniqueness checks. The other S83 duties remain active. The published G3 sources remain byte-exact.

The unchanged PRIV-003 obligation expressly allows a narrower non-identifying public relationship when defined by the governing published generation. This candidate supplies the proposed successor definitions; publication has not occurred. No current deployed behavior is authorized by this construction.

<a id="root"></a>
## root

Equality of public r values MAY express only their shared membership-root relationship when both exact canonical root values and independently authenticated owning source meaning and membership scope agree.

<a id="action"></a>
## action

Equality of public a values MAY express only a shared public action context when both exact canonical values and independently authenticated owning action-context meaning and scope agree.

<a id="duplicate"></a>
## duplicate

Equality of public n values MAY express duplicate recognition only as equality of the scoped pair (a,n), with the same independently authenticated action-context meaning, exact a value and owning uniqueness scope; it MUST NOT permit a cross-action nullifier join.

<a id="bindings"></a>
## bindings

Each permitted public relationship MUST bind the exact declared public-input role, canonical in-domain scalar bytes, occurrence-local field identity and independently authenticated source/scope references; missing or inconsistent binding evidence MUST fail without granting the permission.

<a id="preservation"></a>
## preservation

These permissions MUST apply only to the matching public equality checks for uniqueness and observer-visible correlation; every edge MUST remain in actor reconstruction, and no permission MUST clear an independent correlation path, create a reusable participant identifier or grant an actor-identification relationship.

<a id="binding-schema"></a>
## Exact source-established binding schema

One binding per declared public PI surface uses exactly: role, owner_source_id, source_sha256, source_anchor, scope_id, value_hex, action_node. role is n, a or r. The graph token's internal template key is context::PUBLIC-PI:role, bound to its actual context; it creates no new protocol subject. The token remains PUBLIC with reuse NONE. value_hex is one complete canonical TSEV1 PE-TSE-UINT value in [0,p), and its SHA-256 equals the token digest. The complete source reference and scope must be independently authenticated; spelling and equality cannot establish authority or scope truth.

For r and a, action_node is NOT-APPLICABLE. For n it identifies the a-role token of that same context. Both a tokens must have matching authenticated action-context domain and exact value before an n relationship is permitted. Both n tokens must independently have matching owning uniqueness domain. Neither r nor a permission is a proof of shared actor, common participant or global identity. Equal numerals belonging to different roles receive no permission.

The binding schema adds source-evidence metadata, not public proof inputs or new public disclosure. It must remain within its source-governed custody boundary and be included in complete evidence/source/observer composition. Full canonical privacy-member integration must bind these fields and their authentication evidence before admission. There is no trust-on-first-use and no caller flag which grants scope authority.

<a id="procedure"></a>
## Exact updated graph procedure

The exact newly authored graph subroutine follows. It is a subroutine of the full mandatory regeneration, source appointment, authentication, universe, visibility and failure-order pipeline; it does not itself verify source signatures or return a profile admission PASS. Missing, inconsistent or out-of-domain role bindings fail. Scope and values are compared exactly, never modulo p. A relationship permission removes only its matching EQUALS edge from the correlation test and its matching pair from the blanket public-uniqueness rejection. It never deletes any edge from the actor graph. Visibility, coalition and alternative-path checks remain mandatory.

The original unbound-root negative vector remains valid: without the required role/source binding no exception exists. The new scoped vectors establish the permitted cases and retained failures. No synthetic source identity in these vectors appoints a real source.

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

SCALAR_MODULUS=21888242871839275222246405745257275088548364400416034343698204186575808495617
def canonical_scalar(raw_hex):
    # Complete canonical TSEV1 UINT; no modular reduction or normalization.
    if not isinstance(raw_hex,str) or len(raw_hex)%2 or not raw_hex or any(c not in '0123456789abcdef' for c in raw_hex):raise ValueError('scalar hex')
    raw=bytes.fromhex(raw_hex);prefix=b'TSEV1'+len(b'PE-TSE-UINT').to_bytes(4,'big')+b'PE-TSE-UINT'+bytes([3])
    # The type identifier length is encoded exactly.
    if not raw.startswith(prefix) or len(raw)<len(prefix)+8:raise ValueError('scalar encoding')
    size=int.from_bytes(raw[len(prefix):len(prefix)+8],'big');body=raw[len(prefix)+8:]
    if len(body)!=size or not body or any(c not in b'0123456789' for c in body) or (len(body)>1 and body[0]==48):raise ValueError('scalar canonical decimal')
    if int(body)>=SCALAR_MODULUS:raise ValueError('scalar domain')
    return raw

def validate_public_bindings(nodes,bindings):
    # Authentication is an external mandatory precondition, as for visibility.
    # Exact structural/value/role joins below do not appoint the supplied source.
    bindings={} if bindings is None else bindings
    if not isinstance(bindings,dict):return {},{'INVALID-ACTION-CONTEXT'}
    valid={};failures=set()
    for key,b in bindings.items():
        try:
            if set(b)!={'role','owner_source_id','source_sha256','source_anchor','scope_id','value_hex','action_node'}:raise ValueError('binding schema')
            role=b['role'];n=nodes[key]
            if role not in ('n','a','r') or key!=n['context']+'::PUBLIC-PI:'+role:raise ValueError('exact public surface')
            if n['exposure']!='PUBLIC' or n['reuse']!='NONE':raise ValueError('role exposure/reuse')
            for name in ('owner_source_id','source_anchor','scope_id'):
                if not isinstance(b[name],str) or not b[name] or any(c not in 'ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789._:#-' for c in b[name]):raise ValueError('source identity')
            if not isinstance(b['source_sha256'],str) or len(b['source_sha256'])!=64 or any(c not in '0123456789abcdef' for c in b['source_sha256']):raise ValueError('source digest')
            raw=canonical_scalar(b['value_hex'])
            if hashlib.sha256(raw).hexdigest()!=n['digest']:raise ValueError('value binding')
            expected=n['context']+'::PUBLIC-PI:a' if role=='n' else 'NOT-APPLICABLE'
            if b['action_node']!=expected:raise ValueError('action binding')
            valid[key]=b
        except (KeyError,ValueError,TypeError):failures.add('INVALID-ACTION-CONTEXT')
    for key,n in nodes.items():
        if any(key==n['context']+'::PUBLIC-PI:'+r for r in ('n','a','r')) and key not in valid:failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
    for b in valid.values():
        if b['role']=='n' and (b['action_node'] not in valid or valid[b['action_node']]['role']!='a'):failures.add('INCOMPLETE-EVIDENCE-UNIVERSE')
    return valid,failures

def public_pair_permitted(a,b,bindings):
    x,y=bindings.get(a),bindings.get(b)
    if x is None or y is None or x['role']!=y['role'] or x['value_hex']!=y['value_hex']:return False
    domain=lambda q:tuple(q[k] for k in ('owner_source_id','source_sha256','source_anchor','scope_id'))
    if domain(x)!=domain(y):return False
    if x['role'] in ('r','a'):return True
    # n may join only as a duplicate within the same source-bound a domain/value.
    xa,ya=bindings.get(x['action_node']),bindings.get(y['action_node'])
    return xa is not None and ya is not None and xa['role']==ya['role']=='a' and domain(xa)==domain(ya) and xa['value_hex']==ya['value_hex']

def graph_checks(nodes,edges,required_views,visibility,public_bindings=None):
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
    bindings,binding_failures=validate_public_bindings(nodes,public_bindings);failures.update(binding_failures)
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
    # Public uniqueness retains its rule, with only S84's scope-checked permissions.
    for a,b in combinations(sorted(public),2):
        x,y=nodes[a],nodes[b]
        if x['context']!=y['context'] and x['digest']==y['digest'] and not (x['reuse']==y['reuse']!='NONE' or public_pair_permitted(a,b,bindings)):failures.add('UNIQUENESS-FAILURE')
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
            permitted=k=='EQUALS' and (nodes[a]['reuse']==nodes[b]['reuse']!='NONE' or public_pair_permitted(a,b,bindings))
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

## Complete updated declaration-template generator

This version adds the twenty-one role-binding metadata surfaces and their joins to the S83 declaration model. These remain confidential source-evidence records, not new public PI. S84 owns this updated generator; S83 retains the historical pre-relationship algorithm for traceability. Every generated row is recomputed from the packaged declarations.

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
```
