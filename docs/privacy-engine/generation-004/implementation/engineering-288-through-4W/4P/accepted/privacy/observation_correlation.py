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
