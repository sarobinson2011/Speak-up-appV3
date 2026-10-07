"""Exact-byte pure signature verification with durable full-prefix reconstruction.

A journal authenticates local execution only. It never appoints the supplied
public key or establishes source competence, scope/ledger qualification/admission.
"""
import contextlib,fcntl,hashlib,hmac,json,math,os,platform,subprocess,time
from pathlib import Path
from large_auth.core import validate_manifest,CHUNK
from large_auth.message import signed_message
from v4_ingest.records import parse
from v4_ingest.wire import SIGN_DOMAIN,signature_line
from link_recovery.cli import atomic_save,read_key,canonical,RecoveryError
ROOT=Path(__file__).resolve().parents[1]
VERSION='CP4G-PURE-RECOVERY-1'
BINARY=ROOT/'crypto_backend/bin/pe-rfc8032-stream'

def sha_file(path):
    h=hashlib.sha256()
    with Path(path).open('rb') as f:
        while b:=f.read(CHUNK):h.update(b)
    return h.hexdigest()

def identity():
    manifest=json.loads((ROOT/'crypto_backend/BUILD-MANIFEST.json').read_bytes())
    actual=sha_file(BINARY)
    if actual!=manifest['binary_sha256']:raise RecoveryError('backend executable identity mismatch')
    files=('pure_auth/controller.py','large_auth/message.py','large_auth/core.py','v4_ingest/wire.py','v4_ingest/records.py','v4_ingest/data/security-fields.tsv','link_recovery/cli.py','crypto_backend/Cargo.toml','crypto_backend/Cargo.lock','crypto_backend/src/main.rs')
    current={p:sha_file(ROOT/p) for p in files}
    for p in ('Cargo.toml','Cargo.lock','src/main.rs'):
        if current['crypto_backend/'+p]!=manifest['sources'][p]:raise RecoveryError('backend source/build identity mismatch')
    return {'version':VERSION,'python':platform.python_version(),'binary_sha256':actual,'build_manifest_sha256':sha_file(ROOT/'crypto_backend/BUILD-MANIFEST.json'),'code':current}

def bounded(path,limit):
    with Path(path).open('rb') as f:b=f.read(limit+1)
    if len(b)>limit:raise RecoveryError('local metadata cap')
    return b

def load(path,key):
    def unique(pairs):
        out={}
        for k,v in pairs:
            if k in out:raise RecoveryError('duplicate journal key')
            out[k]=v
        return out
    try:
        raw=json.loads(bounded(path,CHUNK),object_pairs_hook=unique)
        if set(raw)!= {'payload','hmac_sha256'}:raise RecoveryError('journal envelope')
        p=raw['payload'];expected=hmac.new(key,canonical(p),hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected,raw['hmac_sha256']):raise RecoveryError('corrupt journal or wrong key')
        if p['format']!=VERSION:raise RecoveryError('journal version')
        return p
    except (KeyError,TypeError,ValueError) as e:raise RecoveryError('invalid journal') from e

def verify_job(job,checkpoint,key_path,public_key,*,resume=False,new_bytes=64*CHUNK,seconds=50,chunk_bytes=65536,progress=None,fault=None):
    if type(new_bytes) is not int or new_bytes<=0 or not math.isfinite(seconds) or seconds<=0 or type(chunk_bytes) is not int or not 1<=chunk_bytes<=CHUNK:raise RecoveryError('positive bounded byte/time limits and <=1 MiB chunks')
    if type(public_key) is not bytes or len(public_key)!=32:raise RecoveryError('exact 32-byte public key')
    began=time.monotonic();deadline=began+seconds;job=Path(job).resolve();base=job.parent
    raw=bounded(job,CHUNK);m=parse(raw);validate_manifest(m,base)
    sigbytes=bounded(base/m['files']['signature.txt']['path'],4096)
    if len(sigbytes)!=m['files']['signature.txt']['bytes'] or hashlib.sha256(sigbytes).hexdigest()!=m['files']['signature.txt']['sha256']:raise RecoveryError('signature file identity mismatch')
    issuer,sig=signature_line(sigbytes)
    total=len(SIGN_DOMAIN)+sum(m['files'][n]['bytes'] for n in ('evidence.tsv','tokens.tsv','links.tsv'))
    if total>=2**64:raise RecoveryError('signed transport length not representable')
    binding={'backend':identity(),'job_path':str(job),'job_sha256':hashlib.sha256(raw).hexdigest(),'public_key':public_key.hex(),'signature':sig.hex(),'signature_issuer':issuer,'signed_message_bytes':total,'files':m['files'],'model':m['model'],'contract':m['contract'],'canonical_model_sha256':m['canonical_model_sha256'],'scope':m['scope'],'phase':m['phase']}
    ck=Path(checkpoint).resolve();ck.parent.mkdir(parents=True,exist_ok=True);key=read_key(key_path)
    with open(str(ck)+'.lock','a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if resume:
            p=load(ck,key)
            if p['binding']!=binding:raise RecoveryError('incompatible backend/key/signature/input/model/contract binding')
        else:
            if ck.exists():raise RecoveryError('checkpoint exists; use resume')
            p={'format':VERSION,'binding':binding,'offset':0,'prefix_sha256':hashlib.sha256(b'').hexdigest(),'sequence':0,'status':'PAUSED','result':None}
            atomic_save(ck,p,key)
        offset=p['offset']
        if type(offset) is not int or not 0<=offset<=total:raise RecoveryError('checkpoint offset')
        limit=min(total,offset+new_bytes)
        # Native reader receives only the complete replayed prefix and exact
        # new bytes, with EOF. SHA-512 state is rebuilt, never imported from SHA-256.
        proc=subprocess.Popen([str(BINARY),'verify',public_key.hex(),sig.hex(),str(total),str(limit)],stdin=subprocess.PIPE,stdout=subprocess.PIPE,stderr=subprocess.PIPE)
        count=0;h=hashlib.sha256();prefix_checked=offset==0;last=time.monotonic();exhausted=False
        iterator=signed_message(m,base,chunk_bytes)
        try:
            if offset==0 and p['prefix_sha256']!=h.hexdigest():raise RecoveryError('empty prefix mismatch')
            for block in iterator:
                pos=0
                while pos<len(block) and count<limit:
                    if time.monotonic()>=deadline:raise RecoveryError('replay/verification deadline; prior journal unchanged')
                    boundary=offset if count<offset else limit
                    n=min(len(block)-pos,boundary-count);piece=block[pos:pos+n]
                    proc.stdin.write(piece);h.update(piece);pos+=n;count+=n
                    if count==offset:
                        if h.hexdigest()!=p['prefix_sha256']:raise RecoveryError('changed consumed prefix')
                        prefix_checked=True
                    if progress and time.monotonic()-last>=5:
                        progress({'phase':'replay' if count<=offset else 'verify','consumed':count,'total':total,'replay_bytes':min(count,offset)});last=time.monotonic()
                if count==limit and limit<total:break
                # On full completion keep exhausting the iterator so its exact
                # per-file SHA/EOF and final file-change guards MUST run.
            else:exhausted=True
            iterator.close()
            if count!=limit or not prefix_checked:raise RecoveryError('incomplete prefix reconstruction')
            proc.stdin.close();proc.stdin=None
            out,err=proc.communicate(timeout=max(.001,deadline-time.monotonic()))
            if len(out)>4096 or len(err)>4096:raise RecoveryError('backend response bound')
            result=json.loads(out)
            if proc.returncode not in (0,3) or result.get('bytes')!=count or result.get('sha256')!=h.hexdigest():raise RecoveryError('backend rejected or consumed identity mismatch: '+err.decode(errors='replace').strip())
            complete=count==total and exhausted and proc.returncode==0 and result.get('verified') is True
            if count==total and not complete:raise RecoveryError('complete verification not established')
            if count<total and (result.get('verified') is not False or proc.returncode!=3):raise RecoveryError('partial verification cannot authenticate')
            # Recheck exact signature/manifest bytes, never metadata alone.
            if bounded(job,CHUNK)!=raw or bounded(base/m['files']['signature.txt']['path'],4096)!=sigbytes:raise RecoveryError('job/signature changed during processing')
            result={'result':'VERIFIED-EXACT-V2-SIGNATURE' if complete else 'PAUSED','cryptographic_signature_verified':complete,'complete_message_sha256':h.hexdigest() if complete else None,'offset':count,'total':total,'prefix_sha256':h.hexdigest(),'replayed_bytes':offset,'new_bytes':count-offset,'seconds':time.monotonic()-began,'backend_sha256':binding['backend']['binary_sha256'],'public_key':public_key.hex(),'signature':sig.hex(),'four_file_outer_acquisition_checked':False,'source_authority_established':False,'actual_qualification_established':False,'profile_admitted':False}
            p.update(offset=count,prefix_sha256=h.hexdigest(),sequence=p['sequence']+1,status=result['result'],result=result)
            atomic_save(ck,p,key,fault=fault)
            if progress:progress({'phase':'durable-checkpoint','consumed':count,'total':total,'verified':complete})
            return result
        except BaseException:
            proc.kill();proc.communicate();raise
        finally:
            iterator.close()
