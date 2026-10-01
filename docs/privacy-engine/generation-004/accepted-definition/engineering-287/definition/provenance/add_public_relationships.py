from pathlib import Path
import shutil
B=Path('PE-G4-correlation-update');O=Path('PE-G4-public-relationships');shutil.copytree(B,O,dirs_exist_ok=True)
p=O/'privacy/observation_correlation.py'
s=p.read_text()
helper='''
SCALAR_MODULUS=21888242871839275222246405745257275088548364400416034343698204186575808495617
def canonical_scalar(raw_hex):
    # Complete canonical TSEV1 UINT; no modular reduction or normalization.
    if not isinstance(raw_hex,str) or len(raw_hex)%2 or not raw_hex or any(c not in '0123456789abcdef' for c in raw_hex):raise ValueError('scalar hex')
    raw=bytes.fromhex(raw_hex);prefix=b'TSEV1'+(11).to_bytes(4,'big')+b'PE-TSE-UINT'+bytes([3])
    # PE-TSE-UINT is eleven ASCII bytes.
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

'''
# Correct literal length is calculated by the author below and checked by vectors.
helper=helper.replace("(11).to_bytes(4,'big')","len(b'PE-TSE-UINT').to_bytes(4,'big')").replace('# PE-TSE-UINT is eleven ASCII bytes.','# The type identifier length is encoded exactly.')
s=s.replace('def graph_checks(nodes,edges,required_views,visibility):',helper+'def graph_checks(nodes,edges,required_views,visibility,public_bindings=None):')
s=s.replace("public={k for k,v in nodes.items() if v['exposure']=='PUBLIC'};actors=", "bindings,binding_failures=validate_public_bindings(nodes,public_bindings);failures.update(binding_failures)\n    public={k for k,v in nodes.items() if v['exposure']=='PUBLIC'};actors=")
s=s.replace("# Original uniqueness obligation is unchanged by correlation approval.","# Public uniqueness retains its rule, with only S84's scope-checked permissions.")
s=s.replace("not (x['reuse']==y['reuse']!='NONE'):failures.add('UNIQUENESS-FAILURE')", "not (x['reuse']==y['reuse']!='NONE' or public_pair_permitted(a,b,bindings)):failures.add('UNIQUENESS-FAILURE')")
s=s.replace("permitted=k=='EQUALS' and nodes[a]['reuse']==nodes[b]['reuse']!='NONE'", "permitted=k=='EQUALS' and (nodes[a]['reuse']==nodes[b]['reuse']!='NONE' or public_pair_permitted(a,b,bindings))")
p.write_text(s)
