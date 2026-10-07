"""Bounded independent >64 MiB signing, verification and recovery evidence."""
import hashlib,json,os,resource,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fixtures.construct import wire
MIB=1048576

def usage():return resource.getrusage(resource.RUSAGE_SELF).ru_maxrss

def child(mode,root):
    start=time.monotonic();root=Path(root);job=root/'input/job.json'
    if mode=='sign':
        from fixtures.auth_jobs import make
        from cryptography.hazmat.primitives.asymmetric.ed25519 import Ed25519PrivateKey
        from cryptography.hazmat.primitives.serialization import Encoding,PublicFormat
        job=make(root/'input');m=json.loads(job.read_bytes());p=job.parent/'links.tsv';block=bytes(range(256))*4096;h=hashlib.sha256()
        with p.open('wb') as f:
            for _ in range(96):f.write(block);h.update(block)
        m['files']['links.tsv'].update(bytes=p.stat().st_size,sha256=h.hexdigest())
        # This signed byte fixture is deliberately not qualified link evidence.
        evidence=job.parent/'evidence.tsv';lines=evidence.read_text().splitlines();header=lines[0].split('\t');row=lines[1].split('\t');row[header.index('links_sha256')]=h.hexdigest();row[header.index('issued_by')]='CP4G-LAB';evidence.write_bytes(('\t'.join(header)+'\n'+'\t'.join(row)+'\n').encode())
        m['files']['evidence.tsv'].update(bytes=evidence.stat().st_size,sha256=hashlib.sha256(evidence.read_bytes()).hexdigest())
        sk=Ed25519PrivateKey.from_private_bytes(bytes(range(32)));pk=sk.public_key().public_bytes(Encoding.Raw,PublicFormat.Raw)
        message=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+b''.join((job.parent/n).read_bytes() for n in ('evidence.tsv','tokens.tsv','links.tsv'))
        sig=sk.sign(message);(root/'public-key.txt').write_text(pk.hex()+'\n');(root/'signature.hex').write_text(sig.hex()+'\n')
        sp=job.parent/'signature.txt';sp.write_bytes(b'CP4G-LAB '+sig.hex().encode()+b'\n');m['files']['signature.txt'].update(bytes=sp.stat().st_size,sha256=hashlib.sha256(sp.read_bytes()).hexdigest())
        obj=hashlib.sha256(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n')
        for n in ('evidence.tsv','tokens.tsv','links.tsv','signature.txt'):
            p=job.parent/n;obj.update(p.stat().st_size.to_bytes(8,'big'))
            with p.open('rb') as f:
                while b:=f.read(131072):obj.update(b)
        m['object_sha256']=obj.hexdigest();job.write_bytes(wire(m))
        r={'result':'PASS','mode':mode,'message_bytes':len(message),'message_sha256':hashlib.sha256(message).hexdigest(),'public_key':pk.hex(),'signature':sig.hex(),'job_manifest':m,'signer':'cryptography 46.0.0 / OpenSSL 3.5.3 one-shot pure Ed25519'}
    elif mode=='reference':
        from tests.test_auth_crypto import openssl_verify
        from large_auth.backend import sodium_verify
        m=json.loads(job.read_bytes());message=b'PE-TSE-PRIVACY-EVIDENCE-V2\n'+b''.join((job.parent/n).read_bytes() for n in ('evidence.tsv','tokens.tsv','links.tsv'));pk=bytes.fromhex((root/'public-key.txt').read_text().strip());sig=bytes.fromhex((root/'signature.hex').read_text().strip());a=openssl_verify(pk,sig,message);b=sodium_verify(pk,sig,message);assert a and b
        r={'result':'PASS','mode':mode,'openssl_pure':a,'libsodium_pure':b,'message_sha256':hashlib.sha256(message).hexdigest()}
    else:
        from pure_auth.controller import verify_job
        from link_recovery.cli import create_key
        key=root/'recovery.key';create_key(key);pk=bytes.fromhex((root/'public-key.txt').read_text().strip());rows=[]
        def go(name,n,resume=False):
            r=verify_job(job,root/name,key,pk,new_bytes=n,resume=resume,seconds=40,chunk_bytes=MIB);rows.append(r);return r
        full=go('full.j',128*MIB);part=go('resumed.j',40*MIB);resumed=go('resumed.j',128*MIB,True)
        assert full['cryptographic_signature_verified'] and not part['cryptographic_signature_verified'] and resumed['cryptographic_signature_verified'];assert full['complete_message_sha256']==resumed['complete_message_sha256']
        r={'result':'PASS','mode':mode,'rows':rows,'message_sha256':full['complete_message_sha256'],'controller_max_rss_kib':usage(),'native_verifier_max_rss_kib':resource.getrusage(resource.RUSAGE_CHILDREN).ru_maxrss,'chunk_limit_bytes':MIB,'native_buffer_bytes':65536}
    r.update(seconds=time.monotonic()-start,max_rss_kib=usage(),profile_admitted=False,full_retained_stream_processed=False);print(json.dumps(r,indent=2))

if __name__=='__main__':
    if len(sys.argv)>1 and sys.argv[1]=='--child':child(sys.argv[2],sys.argv[3])
    else:
        rows=[];total=0
        with tempfile.TemporaryDirectory(prefix='cp4g-large-') as d:
            for mode in ('sign','reference','stream'):
                start=time.monotonic()
                try:
                    p=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child',mode,d],cwd=ROOT,capture_output=True,text=True,timeout=min(60,180-total))
                    elapsed=time.monotonic()-start;total+=elapsed
                    row=json.loads(p.stdout) if p.returncode==0 else {'result':'FAIL','stderr':p.stderr,'mode':mode};row['bounded_child_wall_seconds']=elapsed;rows.append(row)
                    if row['result']!='PASS':break
                except subprocess.TimeoutExpired:
                    total+=time.monotonic()-start;rows.append({'mode':mode,'result':'TIMEOUT'});break
            disk=sum(p.stat().st_size for p in Path(d).rglob('*') if p.is_file())
        ok=len(rows)==3 and all(r['result']=='PASS' for r in rows) and len({r['message_sha256'] for r in rows})==1
        report={'result':'PASS' if ok else 'FAIL','synthetic_payload_bytes':96*MIB,'rows':rows,'aggregate_benchmark_seconds':total,'per_child_limit_seconds':60,'aggregate_limit_seconds':180,'temporary_disk_bytes':disk,'synthetic_not_conforming_link_stream':True,'profile_admitted':False,'full_retained_stream_processed':False}
        target=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'results/4G-large-message.json';target.write_text(json.dumps(report,indent=2)+'\n');print(json.dumps(report,indent=2));sys.exit(0 if ok else 1)
