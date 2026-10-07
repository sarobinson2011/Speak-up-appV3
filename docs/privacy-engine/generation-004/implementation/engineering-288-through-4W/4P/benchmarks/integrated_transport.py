"""Independent >64 MiB conforming supplied-set fixture, not a ledger witness."""
import sys,json,time,resource,hashlib
from pathlib import Path
from fixtures.construct import wire,sha,l64
from v4_ingest.wire import TOKEN_HEADER,LINK_HEADER,EVIDENCE_HEADER

def make(root):
    from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
    from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
    root.mkdir(parents=True,exist_ok=True);n=512;ids=[f'N{i:06}-'+'a'*262 for i in range(n)]
    tokens=[{'index':i,'id':ids[i],'surface':'LAB:A' if i%2==0 else 'LAB:B','context':'SYMBOLIC-U-ONE' if i<n//2 else 'SYMBOLIC-U-TWO','record':'LAB','exposure':'CONFIDENTIAL','reuse':'NONE','arbitrary':True,'symbolic_digest':sha(b'ARBITRARY')} for i in range(n)]
    pairhash=hashlib.sha256(b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n')
    with (root/'links.tsv').open('wb') as f:
        f.write(('\t'.join(LINK_HEADER)+'\n').encode());ordinal=0
        for i in range(n):
            for j in range(i+1,n):
                pairhash.update(i.to_bytes(4,'big')+j.to_bytes(4,'big'));ordinal+=1
                f.write((f'{ordinal:06}\t{ids[i]}\t{ids[j]}\t000000\tEQUALS\n').encode())
                if (i,j) in ((0,1),(256,257)):
                    ordinal+=1;f.write((f'{ordinal:06}\t{ids[i]}\t{ids[j]}\t000001\tSOURCE\n').encode())
    rows=n*(n-1)//2
    model={'surfaces':[{'node_id':s,'declared_exposure':'CONFIDENTIAL','reuse':'NONE'} for s in ('LAB:A','LAB:B')],'relations':[{'from_node':'LAB:A','to_node':'LAB:B','relation':'SOURCE'}],'tokens':tokens,'structural_edges':[[0,1,1,'SOURCE'],[256,257,1,'SOURCE']],
      'equality_stream':{'format':'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1','row_encoding':'U32-BE left index; U32-BE right index','ordering':'lexicographic index pairs, i<j','predicate':'left.arbitrary OR right.arbitrary OR equal symbolic_digest','rows':rows,'sha256':pairhash.hexdigest(),'bytes':len(b'PE-G4-POTENTIAL-EQUALITY-PAIRS-V1\n')+8*rows},'actor_graph_policy':'ALL structural and equality edges; no visibility/permission filtering'}
    def put(name,b):
        (root/name).write_bytes(b);return entry(name)
    def entry(name):
        from link_recovery.cli import sha as file_sha
        p=root/name;return {'path':name,'bytes':p.stat().st_size,'sha256':file_sha(p)}
    tb=('\t'.join(TOKEN_HEADER)+'\n'+''.join('\t'.join([f'{i+1:06}',t['surface'],t['context'],t['id'],t['symbolic_digest'],t['exposure'],t['reuse']])+'\n' for i,t in enumerate(tokens))).encode()
    files={'tokens.tsv':put('tokens.tsv',tb),'links.tsv':entry('links.tsv')};pid='PE-G4-TSE-PROFILE-000401-V0001'
    outer=b'PE-TSE-IMMUTABLE-PROFILE-V1\n'+b''.join(l64(n.encode())+l64(wire({'transport_fixture':n})) for n in ('SOURCE-OWNED-BODY','EXPRESSION-PROGRAM','PRIVACY'));oe=put('outer.bin',outer)
    ev=('\t'.join(EVIDENCE_HEADER)+'\n'+'\t'.join([pid+'#ADMISSION-COMPOSITION-ALL','ADMISSION-COMPOSITION',pid,sha(outer),pid+'#ADMISSION-V1','NOT-APPLICABLE',sha(wire(model['surfaces'])),sha(wire(model['relations'])),files['tokens.tsv']['sha256'],files['links.tsv']['sha256'],'PASS','PASS','PASS','LAB-AUTH','ED25519-RFC8032'])+'\n').encode();files['evidence.tsv']=put('evidence.tsv',ev)
    key=Ed25519PrivateKey.from_private_bytes(b'4H independent synthetic fixture')
    message=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+ev+tb+(root/'links.tsv').read_bytes();sig=key.sign(message);key.public_key().verify(sig,message)
    # Independent established verifier verifies original pure message, not its digest.
    from large_auth.backend import sodium_verify
    pub=key.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw);assert sodium_verify(pub,sig,message)
    files['signature.txt']=put('signature.txt',b'LAB-AUTH '+sig.hex().encode()+b'\n')
    h=hashlib.sha256(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n')
    for name in ('evidence.tsv','tokens.tsv','links.tsv','signature.txt'):
        h.update(files[name]['bytes'].to_bytes(8,'big'))
        with (root/name).open('rb') as f:
            while b:=f.read(65536):h.update(b)
    job={'format':'CP4F-EXACT-BYTE-JOB-1','files':{'outer':oe,**files},'object_sha256':h.hexdigest(),'profile_sha256':sha(outer),'model':put('model.json',wire(model)),'contract':put('contract.json',wire({'fixture':'independent transport only'})),'scope':'NOT-APPLICABLE','phase':'STATIC-ADMISSION','canonical_model_sha256':sha(wire(model))};put('job.json',wire(job));put('public.json',wire({'public_key':pub.hex()}))
    return {'message_bytes':len(message),'message_sha256':sha(message),'links':files['links.tsv'],'potential_rows':rows,'structural_rows':2,'independent_OpenSSL_and_libsodium_verification':True,'complete_collector_witness':False}

def validate(root):
    from pure_auth.preflight import run
    from link_recovery.cli import create_key,read_key
    from integrated_auth.collector import Adapter
    from integrated_auth.adapters import TokenMatcher
    from admission_kernel.model import Model
    from scope_auth.closure import ScopedModel
    key=root/'journal.key';create_key(key);job=json.loads((root/'job.json').read_bytes());pub=bytes.fromhex(json.loads((root/'public.json').read_bytes())['public_key'])
    r=run(root/'job.json',root/'auth',key,pub,new_bytes=2**30,seconds=45);assert r['cryptographic_signature_verified']
    model=Model(json.loads((root/'model.json').read_bytes()));s=ScopedModel(model,list(range(len(model.tokens))))
    p={'stages':{},'sequence':0};m={'bundles':{'NOT-APPLICABLE':{'files':{k:v for k,v in job['files'].items() if k!='outer'}}}}
    a=Adapter(m,root,root/'semantic',key,p,read_key(key),2**30,45,65536,None)
    link=a.scoped_files('NOT-APPLICABLE',s,{'phase':'STATIC-ADMISSION'},None,None)
    assert link['potential_rows']==130816 and link['structural_rows']==2
    return {'crypto':r['crypto_stage'],'supplied_set':link,'complete_collector_witness':False,'profile_admitted':False}

if __name__=='__main__':
    start=time.monotonic();mode=sys.argv[1];r=(make if mode=='make' else validate)(Path(sys.argv[2]).resolve());r.update(mode=mode,seconds=time.monotonic()-start,peak_rss_kib=resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,child_peak_rss_kib=resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss);print(json.dumps(r,indent=2))
