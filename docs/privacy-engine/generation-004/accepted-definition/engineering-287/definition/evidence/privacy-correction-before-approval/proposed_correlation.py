"""Unadopted G4 correction prototype. No source appointment or live evidence supplied.

Input visibility must already be independently source-validated. Values here are
synthetic author vectors, never evidence. Full actor graph is never filtered.
"""
from itertools import combinations

def assess(nodes,edges,views,coalitions):
    # nodes[id] = context, exposure, reuse. Edges are a,b,relation.
    # views[name] = observed node set, observed edge-index set, complete bool.
    # coalitions explicitly enumerate the threat-model observer combinations.
    if not nodes or not views or not coalitions:return 'INCOMPLETE-SOURCE-MODEL'
    if any(a not in nodes or b not in nodes or a==b for a,b,k in edges):return 'INVALID-GRAPH'
    publics={n for n,v in nodes.items() if v['exposure']=='PUBLIC'}
    actors={n for n,v in nodes.items() if v['exposure']=='PRIVATE-ACTOR'}
    if any(not v['complete'] for v in views.values()):return 'INCOMPLETE-VISIBILITY-EVIDENCE'
    for v in views.values():
        if not set(v['nodes'])<=set(nodes) or not publics<=set(v['nodes']):return 'INVALID-VISIBILITY-MODEL'
        for i in v['edges']:
            if not isinstance(i,int) or not 0<=i<len(edges):return 'INVALID-VISIBILITY-MODEL'
            if not set(edges[i][:2])<=set(v['nodes']):return 'INVALID-VISIBILITY-MODEL'
    if any(not c or not set(c)<=set(views) for c in coalitions):return 'INCOMPLETE-THREAT-MODEL'
    def connected(start,allowed_edges):
        graph={n:set() for n in nodes}
        for a,b,k in allowed_edges:graph[a].add(b);graph[b].add(a)
        seen=set();todo=[start]
        while todo:
            n=todo.pop()
            if n in seen:continue
            seen.add(n);todo.extend(graph[n]-seen)
        return seen
    # Entire actor graph, including constants and confidential paths.
    if any(connected(n,edges)&actors for n in publics):return 'ACTOR-RECONSTRUCTION-RISK'
    def permitted(e):
        a,b,k=e
        return k=='EQUALS' and nodes[a]['reuse']==nodes[b]['reuse']!='NONE'
    for coalition in coalitions:
        visible_edges=set().union(*(set(views[v]['edges']) for v in coalition))
        correlation_edges=[edges[i] for i in sorted(visible_edges) if not permitted(edges[i])]
        for a,b in combinations(sorted(publics),2):
            if nodes[a]['context']!=nodes[b]['context'] and b in connected(a,correlation_edges):return 'CORRELATION-FAILURE'
    return 'PASS-BOUNDED-PROPOSED-GRAPH-CHECKS'

def tests():
    def node(context,exposure='PUBLIC',reuse='NONE'):return dict(context=context,exposure=exposure,reuse=reuse)
    n={'u1':node('ONE'),'u2':node('TWO'),'internal':node('ONE','CONFIDENTIAL')}
    e=[('u1','internal','EQUALS'),('internal','u2','EQUALS')]
    external={'nodes':{'u1','u2'},'edges':set(),'complete':True}
    assert assess(n,e,{'external':external},[('external',)])=='PASS-BOUNDED-PROPOSED-GRAPH-CHECKS'
    observing={'nodes':set(n),'edges':{0,1},'complete':True}
    assert assess(n,e,{'external':observing},[('external',)])=='CORRELATION-FAILURE'
    unknown=dict(external,complete=False)
    assert assess(n,e,{'external':unknown},[('external',)])=='INCOMPLETE-VISIBILITY-EVIDENCE'
    # Known public equality is not excused just because it is a root, a or n.
    assert assess(n,[('u1','u2','EQUALS')],{'external':dict(external,edges={0})},[('external',)])=='CORRELATION-FAILURE'
    # Individually incomplete paths compose under an admitted collusion model.
    left={'nodes':set(n),'edges':{0},'complete':True};right={'nodes':set(n),'edges':{1},'complete':True}
    assert assess(n,e,{'left':left,'right':right},[('left','right')])=='CORRELATION-FAILURE'
    # A confidential unobservable path cannot be removed from actor testing.
    na=dict(n,actor=node('ONE','PRIVATE-ACTOR'));ea=e+[('internal','actor','DERIVES')]
    assert assess(na,ea,{'external':external},[('external',)])=='ACTOR-RECONSTRUCTION-RISK'
    # Even a permitted constant equality remains in the actor graph.
    nb={'public':node('ONE',reuse='GENERATION-CONSTANT'),'actor':node('TWO','PRIVATE-ACTOR','GENERATION-CONSTANT')}
    vb={'nodes':{'public'},'edges':set(),'complete':True}
    assert assess(nb,[('public','actor','EQUALS')],{'external':vb},[('external',)])=='ACTOR-RECONSTRUCTION-RISK'
    print('PASS — seven bounded correction vectors; proposed rule remains unadopted.')

if __name__=='__main__':tests()
