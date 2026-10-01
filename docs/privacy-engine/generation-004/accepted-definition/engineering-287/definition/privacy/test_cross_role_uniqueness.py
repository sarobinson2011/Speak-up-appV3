from pathlib import Path
import runpy,copy,contextlib,io,json
O=Path(__file__).resolve().parents[1];M=runpy.run_path(str(O/'privacy/cross_role_uniqueness.py'))
with contextlib.redirect_stdout(io.StringIO()):V=runpy.run_path(str(O/'privacy/test_public_relationships.py'))
n,e,b=V['fixture'](('r','a'),{'r':(7,7),'a':(7,7)})
e += [('U1::PUBLIC-PI:r','U2::PUBLIC-PI:a','EQUALS'),('U1::PUBLIC-PI:a','U2::PUBLIC-PI:r','EQUALS')]
views=[('public',)]
def vis(nodes,edges):return {views[0]:{'nodes':{k:'VISIBLE' if v['exposure']=='PUBLIC' else 'HIDDEN' for k,v in nodes.items()},'edges':{i:'VISIBLE' if nodes[a]['exposure']==nodes[z]['exposure']=='PUBLIC' else 'HIDDEN' for i,(a,z,_) in enumerate(edges)}}}
def proofs(nodes,edges,bindings,pairs):
 domain=lambda q:{k:q[k] for k in ('role','owner_source_id','source_sha256','source_anchor','scope_id')}
 return [{'evidence_id':f'SEP-{i}','left_node':a,'right_node':z,'left_domain':domain(bindings[a]),'right_domain':domain(bindings[z]),'owner_source_id':'FIXTURE-SOURCE','source_sha256':'ab'*32,'source_anchor':'separation','graph_sha256':M['C']['graph_digest'](nodes,edges),'scope':'CROSS-ROLE-RAW-SCALAR-CORRELATION-ONLY','separate_semantic_domains':True,'no_source_defined_linkage':True} for i,(a,z) in enumerate(pairs)]
pairs=[x[:2] for x in e[-2:]];p=proofs(n,e,b,pairs);results=[]
def assess(name,ns=None,es=None,bs=None,ps=None,auth=None,origins=None,matrix=None):
 ns=n if ns is None else ns;es=e if es is None else es;bs=b if bs is None else bs;ps=p if ps is None else ps
 r=M['graph_checks'](ns,es,views,vis(ns,es) if matrix is None else matrix,bs,ps,{x['evidence_id'] for x in ps} if auth is None else auth,{i:'RAW-SCALAR-EQUALITY' for i in range(len(es))} if origins is None else origins)
 results.append({'case':name,**r});return r
r=assess('all distinct-role pairs qualified');assert r['failures']==[] and r['profile_admitted'] is False
r=assess('one qualified pair cannot hide second collision',ps=p[:1]);assert 'UNIQUENESS-FAILURE' in r['failures'] and 'CORRELATION-FAILURE' in r['failures']
for name,kw,failure in [('no claims',{'ps':[]},'UNIQUENESS-FAILURE'),('unauthenticated claims',{'auth':set()},'INVALID-EVIDENCE-AUTHENTICATION'),('unknown provenance',{'origins':{}},'INCOMPLETE-EVIDENCE-UNIVERSE'),('source-established pair',{'origins':{i:'SOURCE-ESTABLISHED' if i==2 else 'RAW-SCALAR-EQUALITY' for i in range(4)}},'INVALID-ACTION-CONTEXT')]:
 r=assess(name,**kw);assert failure in r['failures'] and 'UNIQUENESS-FAILURE' in r['failures']
for field,value in [('left_domain',{}),('graph_sha256','00'*32),('separate_semantic_domains',None),('no_source_defined_linkage',False),('scope','GLOBAL-UNIQUENESS-WAIVER')]:
 q=copy.deepcopy(p);q[0][field]=value;r=assess('reject '+field,ps=q);assert r['failures'] and 'UNIQUENESS-FAILURE' in r['failures']
x=vis(n,e);x[views[0]]['edges'][2]='UNKNOWN';r=assess('unknown visibility remains a failure',matrix=x);assert 'INCOMPLETE-EVIDENCE-UNIVERSE' in r['failures']
# Hidden actors never disappear from the original full-graph assessment.
n2=copy.deepcopy(n);n2['actor']={'context':'U1','exposure':'PRIVATE-ACTOR','reuse':'NONE','digest':'ef'*32};e2=e+[(pairs[0][0],'actor','DERIVES')];p2=proofs(n2,e2,b,pairs)
r=assess('hidden actor bridge retained',ns=n2,es=e2,ps=p2,origins={i:'STRUCTURAL' if i==4 else 'RAW-SCALAR-EQUALITY' for i in range(5)});assert 'ACTOR-RECONSTRUCTION-RISK' in r['failures']
n2=copy.deepcopy(n);n2['bridge']={'context':'U1','exposure':'PUBLIC','reuse':'NONE','digest':'ef'*32};e2=e+[(pairs[0][0],'bridge','REFERENCES'),('bridge',pairs[0][1],'REFERENCES')];p2=proofs(n2,e2,b,pairs)
r=assess('alternate observable source path retained',ns=n2,es=e2,ps=p2,origins={i:'STRUCTURAL' if i>=4 else 'RAW-SCALAR-EQUALITY' for i in range(6)});assert 'CORRELATION-FAILURE' in r['failures']
n2,e2,b2=V['fixture'](('a','n'),{'a':(11,12),'n':(13,13)});p2=proofs(n2,e2,b2,[('U1::PUBLIC-PI:n','U2::PUBLIC-PI:n')]);r=assess('same-role cross-action nullifier stays rejected',ns=n2,es=e2,bs=b2,ps=p2);assert 'UNIQUENESS-FAILURE' in r['failures'] and 'CORRELATION-FAILURE' in r['failures']
# Additional equal public value outside claimed pairs still fails uniqueness.
n2=copy.deepcopy(n);n2['U2::UNRELATED']=dict(n['U2::PUBLIC-PI:r']);e2=e+[('U1::PUBLIC-PI:r','U2::UNRELATED','EQUALS')];p2=proofs(n2,e2,b,pairs)
r=assess('unrelated public collision cannot borrow permission',ns=n2,es=e2,ps=p2);assert 'UNIQUENESS-FAILURE' in r['failures']
report={'author_checks':'PASS','synthetic_evidence_only':True,'vectors':results,'source_evidence_authenticated':False,'profile_admitted':False}
(O/'verification/cross-role-uniqueness.json').write_text(json.dumps(report,indent=2)+'\n')
print('PASS — '+str(len(results))+' uniqueness correction vectors; every other offending pair remains checked.')
print('PASS — full actor graph, source-established linkage and unknown-evidence failures retained.')
print('BOUNDARY — source/visibility evidence and governing profile admission remain unestablished.')
