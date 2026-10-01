"""Synthetic author vectors for the three approved public relationships."""
from pathlib import Path
import runpy,copy,hashlib,json
M=runpy.run_path(str(Path(__file__).with_name('observation_correlation.py')))
check=M['graph_checks'];p=M['SCALAR_MODULUS']
def scalar(v):
    t=b'PE-TSE-UINT';body=str(v).encode();return (b'TSEV1'+len(t).to_bytes(4,'big')+t+b'\x03'+len(body).to_bytes(8,'big')+body).hex()
def fixture(roles=('r',),values=None):
    values=values or {'r':(7,7),'a':(11,11),'n':(13,13)}
    nodes={};bind={};edges=[]
    for role in roles:
        for i,ctx in enumerate(('U1','U2')):
            key=ctx+'::PUBLIC-PI:'+role;raw=scalar(values[role][i]);nodes[key]={'context':ctx,'exposure':'PUBLIC','reuse':'NONE','digest':hashlib.sha256(bytes.fromhex(raw)).hexdigest()}
            bind[key]={'role':role,'owner_source_id':'PE-G4-SOURCE-S84','source_sha256':'ab'*32,'source_anchor':'fixture-'+role,'scope_id':'fixture-scope-'+role,'value_hex':raw,'action_node':ctx+'::PUBLIC-PI:a' if role=='n' else 'NOT-APPLICABLE'}
        if values[role][0]==values[role][1]:edges.append(('U1::PUBLIC-PI:'+role,'U2::PUBLIC-PI:'+role,'EQUALS'))
    return nodes,edges,bind
V=[('public',)]
def assess(n,e,b,hidden=()):
    matrix={V[0]:{'nodes':{k:'HIDDEN' if k in hidden else 'VISIBLE' for k in n},'edges':{i:'HIDDEN' if a in hidden or z in hidden else 'VISIBLE' for i,(a,z,_) in enumerate(e)}}}
    return check(n,e,V,matrix,b)
results=[]
def expect(name,n,e,b,wanted,hidden=()):
    r=assess(n,e,b,hidden);assert r['earliest_failure']==wanted,(name,r);results.append({'case':name,**r});return r
n,e,b=fixture();expect('shared root in exact same source scope permitted',n,e,b,'NONE')
n,e,b=fixture(('a',));expect('shared public action context permitted',n,e,b,'NONE')
n,e,b=fixture(('a','n'));expect('same scoped a and n duplicate permitted',n,e,b,'NONE')
n,e,b=fixture(('r','a','n'));expect('all three compose without actor edge',n,e,b,'NONE')
n,e,b=fixture();b['U2::PUBLIC-PI:r']['scope_id']='another-membership-scope';expect('same root value different scope rejected',n,e,b,'UNIQUENESS-FAILURE')
n,e,b=fixture();b['U2::PUBLIC-PI:r']['source_sha256']='cd'*32;expect('different root source bytes not equated',n,e,b,'UNIQUENESS-FAILURE')
n,e,b=fixture(('a',));b['U2::PUBLIC-PI:a']['scope_id']='another-action-domain';expect('same numeric a different domain rejected',n,e,b,'UNIQUENESS-FAILURE')
n,e,b=fixture(('a','n'),{'a':(11,12),'n':(13,13)});r=expect('n across different a rejected',n,e,b,'UNIQUENESS-FAILURE');assert 'CORRELATION-FAILURE' in r['failures']
n,e,b=fixture(('a','n'));b['U2::PUBLIC-PI:n']['scope_id']='another-uniqueness-scope';expect('same a and n different uniqueness domain rejected',n,e,b,'UNIQUENESS-FAILURE')
n,e,b=fixture(('n',));expect('n without exact a bindings fails closed',n,e,b,'INCOMPLETE-EVIDENCE-UNIVERSE')
n,e,b=fixture();del b['U2::PUBLIC-PI:r'];expect('missing root scope evidence fails closed',n,e,b,'INCOMPLETE-EVIDENCE-UNIVERSE')
n,e,b=fixture();b['U1::PUBLIC-PI:r']['value_hex']=scalar(8);expect('claim value digest mismatch rejected',n,e,b,'INVALID-ACTION-CONTEXT')
n,e,b=fixture();b['U1::PUBLIC-PI:r']['value_hex']=scalar(p);n['U1::PUBLIC-PI:r']['digest']=hashlib.sha256(bytes.fromhex(scalar(p))).hexdigest();expect('out of scalar domain rejected',n,e,b,'INVALID-ACTION-CONTEXT')
n,e,b=fixture();n['U1::PUBLIC-PI:r']['reuse']='GENERATION-CONSTANT';expect('root cannot be relabelled generation constant',n,e,b,'INVALID-ACTION-CONTEXT')
n,e,b=fixture();b['U1::PUBLIC-PI:r']['action_node']='invented';expect('unexpected relationship metadata rejected',n,e,b,'INVALID-ACTION-CONTEXT')
n,e,b=fixture();b['U1::PUBLIC-PI:r']['role']='a';expect('cross-role reinterpretation rejected',n,e,b,'INVALID-ACTION-CONTEXT')
n,e,b=fixture(('a','n'));b['U1::PUBLIC-PI:n']['action_node']='U2::PUBLIC-PI:a';expect('cannot borrow other occurrence a binding',n,e,b,'INVALID-ACTION-CONTEXT')
# A valid relationship NEVER removes any edge from actor reconstruction.
n,e,b=fixture();n['actor']={'context':'U1','exposure':'PRIVATE-ACTOR','reuse':'NONE','digest':hashlib.sha256(b'actor').hexdigest()};e.append(('U2::PUBLIC-PI:r','actor','DERIVES'));expect('permitted root edge remains in full actor graph',n,e,b,'ACTOR-RECONSTRUCTION-RISK',('actor',))
# Extra visible bridge remains forbidden even when root equality is permitted.
n,e,b=fixture();n['bridge']={'context':'U1','exposure':'CONFIDENTIAL','reuse':'NONE','digest':hashlib.sha256(b'bridge').hexdigest()};e.extend([('U1::PUBLIC-PI:r','bridge','REFERENCES'),('bridge','U2::PUBLIC-PI:r','REFERENCES')]);expect('permission does not clear an alternative correlation path',n,e,b,'CORRELATION-FAILURE')
# Raw value collision between distinct public roles is not an approved relation.
n,e,b=fixture(('r','a'),{'r':(7,7),'a':(7,7)});e.append(('U1::PUBLIC-PI:r','U2::PUBLIC-PI:a','EQUALS'));expect('cross-role scalar equality receives no permission',n,e,b,'UNIQUENESS-FAILURE')
# U itself cannot be assigned one of the three role permissions.
n,e,b=fixture();n['unrelated']=dict(n['U1::PUBLIC-PI:r']);b['unrelated']=dict(b['U1::PUBLIC-PI:r']);expect('unrelated subject cannot acquire root permission',n,e,b,'INVALID-ACTION-CONTEXT')
if __name__=='__main__':
    print('PASS — '+str(len(results))+' scoped public-relationship vectors.')
    print('PASS — cross-action nullifier links, actor paths and alternative correlation paths still fail.')
    print('Bounded author checks only; no source appointment or profile admission.')
