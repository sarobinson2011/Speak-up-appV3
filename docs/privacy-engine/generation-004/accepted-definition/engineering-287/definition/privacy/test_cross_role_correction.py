from pathlib import Path
import runpy,copy,contextlib,io,json
O=Path(__file__).resolve().parents[1]
M=runpy.run_path(str(O/'privacy/cross_role_correlation.py'))
with contextlib.redirect_stdout(io.StringIO()):V=runpy.run_path(str(O/'privacy/test_public_relationships.py'))
n,e,b=V['fixture'](('r','a'),{'r':(7,7),'a':(7,7)})
e.append(('U1::PUBLIC-PI:r','U2::PUBLIC-PI:a','EQUALS'))
views=[('public',)]
def visibility(nodes,edges):return {views[0]:{'nodes':{k:'VISIBLE' if v['exposure']=='PUBLIC' else 'HIDDEN' for k,v in nodes.items()},'edges':{i:'VISIBLE' if nodes[a]['exposure']==nodes[z]['exposure']=='PUBLIC' else 'HIDDEN' for i,(a,z,_) in enumerate(edges)}}}
a,z=e[-1][:2];domain=lambda q:{k:q[k] for k in ('role','owner_source_id','source_sha256','source_anchor','scope_id')}
p={'evidence_id':'SEPARATION-ONE','left_node':a,'right_node':z,'left_domain':domain(b[a]),'right_domain':domain(b[z]),'owner_source_id':'FIXTURE-SOURCE','source_sha256':'ab'*32,'source_anchor':'separation','graph_sha256':M['graph_digest'](n,e),'scope':'CROSS-ROLE-RAW-SCALAR-CORRELATION-ONLY','separate_semantic_domains':True,'no_source_defined_linkage':True}
results=[]
def run(name,proof=None,auth=None,origins=None,nodes=None,edges=None,bind=None,vis=None):
 nodes=n if nodes is None else nodes;edges=e if edges is None else edges
 r=M['graph_checks'](nodes,edges,views,visibility(nodes,edges) if vis is None else vis,b if bind is None else bind,[p] if proof is None else proof,{'SEPARATION-ONE'} if auth is None else auth,{i:'RAW-SCALAR-EQUALITY' for i in range(len(edges))} if origins is None else origins)
 assert r.get('full_actor_graph_preserved',True);results.append({'case':name,**r});return r
r=run('authenticated distinct roles: correlation-only correction');assert 'CORRELATION-FAILURE' not in r['failures'] and 'UNIQUENESS-FAILURE' in r['failures']
for name,kwargs,failure in [('missing authentication',{'auth':set()},'INVALID-EVIDENCE-AUTHENTICATION'),('missing provenance',{'origins':{}},'INCOMPLETE-EVIDENCE-UNIVERSE'),('source-established equality',{'origins':{0:'RAW-SCALAR-EQUALITY',1:'RAW-SCALAR-EQUALITY',2:'SOURCE-ESTABLISHED'}},'INVALID-ACTION-CONTEXT')]:
 r=run(name,**kwargs);assert failure in r['failures'] and 'CORRELATION-FAILURE' in r['failures']
for field,value in [('separate_semantic_domains',None),('no_source_defined_linkage',False),('scope','ALL-EQUALITY'),('graph_sha256','00'*32),('left_domain',{})]:
 q=copy.deepcopy(p);q[field]=value;r=run('reject '+field,proof=[q]);assert 'CORRELATION-FAILURE' in r['failures']
r=run('no claim preserves baseline',proof=[]);assert 'CORRELATION-FAILURE' in r['failures']
# New direct/indirect source path survives raw-equality correction.
n2=copy.deepcopy(n);n2['bridge']={'context':'U1','exposure':'PUBLIC','reuse':'NONE','digest':'ef'*32};e2=e+[(a,'bridge','REFERENCES'),('bridge',z,'REFERENCES')];q=copy.deepcopy(p);q['graph_sha256']=M['graph_digest'](n2,e2)
r=run('observable source path remains',proof=[q],nodes=n2,edges=e2,origins={i:'RAW-SCALAR-EQUALITY' if i<3 else 'STRUCTURAL' for i in range(len(e2))});assert 'CORRELATION-FAILURE' in r['failures']
n2=copy.deepcopy(n);n2['actor']={'context':'U1','exposure':'PRIVATE-ACTOR','reuse':'NONE','digest':'ef'*32};e2=e+[(z,'actor','DERIVES')];q=copy.deepcopy(p);q['graph_sha256']=M['graph_digest'](n2,e2)
r=run('hidden actor path retained',proof=[q],nodes=n2,edges=e2,origins={i:'RAW-SCALAR-EQUALITY' if i<3 else 'STRUCTURAL' for i in range(len(e2))});assert 'ACTOR-RECONSTRUCTION-RISK' in r['failures']
vis=visibility(n,e);vis[views[0]]['edges'][2]='UNKNOWN';r=run('unknown visibility fails',vis=vis);assert 'INCOMPLETE-EVIDENCE-UNIVERSE' in r['failures']
n3,e3,b3=V['fixture'](('a','n'),{'a':(11,12),'n':(13,13)});q=copy.deepcopy(p);q.update(left_node='U1::PUBLIC-PI:n',right_node='U2::PUBLIC-PI:n',left_domain=domain(b3['U1::PUBLIC-PI:n']),right_domain=domain(b3['U2::PUBLIC-PI:n']),graph_sha256=M['graph_digest'](n3,e3))
r=run('cross-action same-role nullifier tracking stays rejected',proof=[q],nodes=n3,edges=e3,bind=b3);assert 'CORRELATION-FAILURE' in r['failures'] and 'INVALID-ACTION-CONTEXT' in r['failures']
(O/'verification/cross-role-correction.json').write_text(json.dumps({'author_checks':'PASS','synthetic_evidence_only':True,'vectors':results,'source_evidence_authenticated':False,'profile_admitted':False},indent=2)+'\n')
print('PASS — 14 cross-role correction vectors; source links, unknown visibility and actor protection retained.')
print('BOUNDARY — uniqueness remains unchanged and still rejects the cross-role public-byte collision.')
