"""Bounded-memory exact outer/four-file bytes and V2 object hashing.

Resume reconstructs live hashlib/parser states by replaying EVERY consumed byte.
A digest is never imported as hash state. Journals authenticate local execution,
not the protocol source. Regular, quiescent files are required.
"""
import contextlib,fcntl,hashlib,json,math,os,platform,stat,time
from pathlib import Path
from v4_ingest.wire import FILES,MEMBERS,PROFILE_DOMAIN,OBJECT_DOMAIN
from v4_ingest.records import exact,primitive,require,ValidationError
from link_recovery.cli import atomic_save,read_key,canonical,RecoveryError,PauseRequested
VERSION='Engineering-288-CP4F-HASH-1'
NAMES=('outer',)+FILES
CHUNK=1024*1024

class Outer:
    def __init__(self):
        self.stage='domain';self.pending=b'';self.index=0;self.remaining=0;self.length=0;self.h=hashlib.sha256();self.members=[]
    def feed(self,data):
        while data:
            if self.stage=='done':raise RecoveryError('trailing outer-container bytes')
            if self.stage=='body':
                n=min(self.remaining,len(data));self.h.update(data[:n]);data=data[n:];self.remaining-=n
                if not self.remaining:
                    self.members.append({'name':MEMBERS[self.index],'bytes':self.length,'sha256':self.h.hexdigest()});self.index+=1
                    self.stage='done' if self.index==3 else 'name-length'
                continue
            need={'domain':len(PROFILE_DOMAIN),'name-length':8,'name':len(MEMBERS[self.index]),'body-length':8}[self.stage]
            n=min(need-len(self.pending),len(data));self.pending+=data[:n];data=data[n:]
            if len(self.pending)!=need:continue
            b=self.pending;self.pending=b''
            if self.stage=='domain':
                if b!=PROFILE_DOMAIN:raise RecoveryError('outer domain')
                self.stage='name-length'
            elif self.stage=='name-length':
                if int.from_bytes(b,'big')!=len(MEMBERS[self.index]):raise RecoveryError('outer member name length')
                self.stage='name'
            elif self.stage=='name':
                if b!=MEMBERS[self.index].encode():raise RecoveryError('outer member order/name')
                self.stage='body-length'
            else:
                self.length=self.remaining=int.from_bytes(b,'big')
                if not self.remaining:raise RecoveryError('empty outer member')
                self.h=hashlib.sha256();self.stage='body'
    def state(self):
        return {'stage':self.stage,'pending':self.pending.hex(),'index':self.index,'remaining':self.remaining,'length':self.length,'member_prefix_sha256':self.h.hexdigest(),'members':self.members}
    def finish(self):
        if self.stage!='done':raise RecoveryError('truncated outer container')

def code_identity():
    root=Path(__file__).resolve().parents[1]
    return {'version':VERSION,'python':platform.python_version(),
            'files':{p:hashlib.sha256((root/p).read_bytes()).hexdigest() for p in ('large_auth/core.py','large_auth/integration.py','large_auth/backend.py','large_auth/message.py','link_recovery/cli.py')}}

def load(path,key):
    import hmac
    with Path(path).open('rb') as stream:raw=stream.read(1024*1024+1)
    if len(raw)>1024*1024:raise RecoveryError('journal size limit')
    def unique(pairs):
        d={}
        for k,v in pairs:
            if k in d:raise RecoveryError('duplicate checkpoint key')
            d[k]=v
        return d
    try:
        x=json.loads(raw,object_pairs_hook=unique)
        if set(x)!={'payload','hmac_sha256'}:raise RecoveryError('journal envelope')
        expected=hmac.new(key,canonical(x['payload']),hashlib.sha256).hexdigest()
        if not hmac.compare_digest(expected,x['hmac_sha256']):raise RecoveryError('journal corruption/wrong key')
        p=x['payload']
        if p['format']!=VERSION or p['code']!=code_identity():raise RecoveryError('incompatible validator/version')
        return p
    except (ValueError,KeyError,TypeError) as e:raise RecoveryError('malformed journal') from e

def validate_manifest(m,base):
    exact(m,('format','files','object_sha256','profile_sha256','model','contract','scope','phase','canonical_model_sha256'))
    require(m['format']=='CP4F-EXACT-BYTE-JOB-1','job format');exact(m['files'],NAMES)
    require(m['scope'] in ('ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE'),'scope')
    require(m['phase'] in ('STATIC-ADMISSION','E','PRE-EXECUTION','PRE-COMMITMENT'),'accepted exact evidence phase',category='INCOMPLETE-EVIDENCE-UNIVERSE')
    for k in ('object_sha256','profile_sha256','canonical_model_sha256'):primitive('DIGEST',m[k])
    for name,e in list(m['files'].items())+[('model',m['model']),('contract',m['contract'])]:
        exact(e,('path','bytes','sha256'));primitive('DIGEST',e['sha256'])
        require(type(e['bytes']) is int and 0<=e['bytes']<2**64,'exact U64 length')
        require(type(e['path']) is str and e['path'] and not Path(e['path']).is_absolute() and '..' not in Path(e['path']).parts,'relative job path')
        require((base/e['path']).resolve().is_relative_to(base),'job path containment')
    require(m['files']['outer']['sha256']==m['profile_sha256'],'expected final outer binding',category='PROFILE-DIGEST-MISMATCH')

def mark(fd):
    s=os.fstat(fd)
    if not stat.S_ISREG(s.st_mode):raise RecoveryError('regular file required')
    return (s.st_dev,s.st_ino,s.st_size,s.st_mtime_ns,s.st_ctime_ns)

def execute(manifest_path,checkpoint,key_path,*,new_bytes=64*CHUNK,seconds=50,chunk_bytes=CHUNK,resume=False,fault=None,progress=None):
    if type(new_bytes) is not int or new_bytes<=0 or not 0<seconds or not math.isfinite(seconds) or type(chunk_bytes) is not int or not 1<=chunk_bytes<=CHUNK:raise RecoveryError('explicit bounded bytes, positive deadline, <=1 MiB chunks required')
    started=time.monotonic();deadline=started+seconds;manifest_path=Path(manifest_path).resolve();base=manifest_path.parent
    with manifest_path.open('rb') as stream:raw=stream.read(CHUNK+1)
    if len(raw)>CHUNK:raise RecoveryError('job manifest local limit')
    from v4_ingest.records import parse
    m=parse(raw);validate_manifest(m,base)
    checkpoint=Path(checkpoint).resolve();checkpoint.parent.mkdir(parents=True,exist_ok=True);key=read_key(key_path)
    binding={'manifest_path':str(manifest_path),'manifest_sha256':hashlib.sha256(raw).hexdigest(),'model':m['model'],'contract':m['contract'],'scope':m['scope'],'phase':m['phase']}
    with open(str(checkpoint)+'.lock','a+b') as lock,contextlib.ExitStack() as stack:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        if resume:
            p=load(checkpoint,key)
            if p['binding']!=binding:raise RecoveryError('incompatible model/contract/input manifest')
            if p['status']=='REJECTED':raise RecoveryError('terminal rejected checkpoint')
        else:
            if checkpoint.exists():raise RecoveryError('checkpoint exists; resume or choose fresh path')
            p={'format':VERSION,'code':code_identity(),'binding':binding,'offsets':[0]*5,'prefixes':[hashlib.sha256(b'').hexdigest()]*5,'outer':Outer().state(),'object_prefix_sha256':None,'sequence':0,'status':'PAUSED','result':None}
        descriptors={};marks={}
        for name,e in list(m['files'].items())+[('model',m['model']),('contract',m['contract'])]:
            fd=os.open(base/e['path'],os.O_RDONLY|os.O_NOFOLLOW);stack.callback(os.close,fd);fcntl.flock(fd,fcntl.LOCK_SH|fcntl.LOCK_NB)
            descriptors[name]=fd;marks[name]=mark(fd)
            if marks[name][2]!=e['bytes']:raise RecoveryError('input size changed: '+name)
        # Pinned descriptor/contract identities; neither is a pair/link stream.
        for name in ('model','contract'):
            h=hashlib.sha256()
            while True:
                if time.monotonic()>=deadline:raise RecoveryError('binding identity deadline; checkpoint unchanged')
                b=os.read(descriptors[name],chunk_bytes)
                if not b:break
                h.update(b)
            if h.hexdigest()!=m[name]['sha256']:raise RecoveryError('changed '+name+' binding')
        outer=Outer();obj=hashlib.sha256(OBJECT_DOMAIN);hs=[hashlib.sha256() for _ in NAMES];offsets=[0]*5
        replayed=0;advanced=0;last=time.monotonic();complete=True;stop=False
        saved_offsets=p['offsets'];require(type(saved_offsets) is list and len(saved_offsets)==5,'journal offsets')
        if not resume:atomic_save(checkpoint,p,key)
        def emit(phase):
            nonlocal last
            if progress:progress({'phase':phase,'offsets':offsets[:],'prefix_bytes_rechecked':replayed,'new_bytes':advanced})
            last=time.monotonic()
        def feed(i,b):
            hs[i].update(b)
            if i==0:outer.feed(b)
            else:obj.update(b)
            offsets[i]+=len(b)
        # Replay is separate from advance, so source mutation cannot be mistaken
        # for a new valid prefix. Live hash/parser states are reconstructed exactly.
        for i,name in enumerate(NAMES):
            size=m['files'][name]['bytes'];offset=saved_offsets[i]
            if type(offset) is not int or not 0<=offset<=size:raise RecoveryError('invalid offset')
            if i and saved_offsets[i-1]!=m['files'][NAMES[i-1]]['bytes'] and offset:raise RecoveryError('nonsequential journal offsets')
            if i:obj.update(size.to_bytes(8,'big'))
            while offsets[i]<offset:
                if time.monotonic()>=deadline:raise RecoveryError('prefix replay deadline; saved checkpoint unchanged')
                b=os.read(descriptors[name],min(chunk_bytes,offset-offsets[i]))
                if not b:raise RecoveryError('truncated prefix')
                feed(i,b);replayed+=len(b)
                if time.monotonic()-last>=5:emit('prefix-replay')
            if hs[i].hexdigest()!=p['prefixes'][i]:raise RecoveryError('changed consumed input prefix: '+name)
        # Prefix framing always includes every length, even future file lengths;
        # to continue the proper V2 order reconstruct only the active prefix below.
        if outer.state()!=p['outer']:raise RecoveryError('outer parser state mismatch')
        # The above per-file replay hashes cannot concatenate length prefixes for
        # future files before earlier data. Reconstruct ordered object hash once.
        obj=hashlib.sha256(OBJECT_DOMAIN)
        for i,name in enumerate(NAMES[1:],1):
            if i>1 and offsets[i-1]<m['files'][NAMES[i-1]]['bytes']:break
            if offsets[0]<m['files']['outer']['bytes']:break
            obj.update(m['files'][name]['bytes'].to_bytes(8,'big'))
            os.lseek(descriptors[name],0,os.SEEK_SET);count=0
            while count<offsets[i]:
                if time.monotonic()>=deadline:raise RecoveryError('object prefix replay deadline; checkpoint unchanged')
                b=os.read(descriptors[name],min(chunk_bytes,offsets[i]-count))
                if not b:raise RecoveryError('truncated object prefix')
                obj.update(b);count+=len(b);replayed+=len(b)
            if offsets[i]<m['files'][name]['bytes']:break
        if resume and p['object_prefix_sha256'] is not None and obj.hexdigest()!=p['object_prefix_sha256']:raise RecoveryError('object prefix identity/state mismatch')
        # No unread read-ahead: every read is bounded by the exact new-byte budget.
        try:
            for i,name in enumerate(NAMES):
                e=m['files'][name];size=e['bytes'];fd=descriptors[name];os.lseek(fd,offsets[i],os.SEEK_SET)
                # Prefixes for a new file must be included exactly once.
                if i and offsets[i]==0 and (not resume or saved_offsets[i-1]<m['files'][NAMES[i-1]]['bytes'] or saved_offsets[0]<m['files']['outer']['bytes']):obj.update(size.to_bytes(8,'big'))
                while offsets[i]<size:
                    if advanced>=new_bytes or time.monotonic()>=deadline:stop=True;break
                    b=os.read(fd,min(chunk_bytes,size-offsets[i],new_bytes-advanced))
                    if not b:raise RecoveryError('truncated input '+name)
                    feed(i,b);advanced+=len(b)
                    if time.monotonic()-last>=5:emit('acquisition')
                if stop:complete=False;break
                if os.read(fd,1):raise RecoveryError('input grew '+name)
                if hs[i].hexdigest()!=e['sha256']:raise RecoveryError('consumed complete file digest mismatch '+name)
                if i==0:outer.finish()
            for name,fd in descriptors.items():
                if mark(fd)!=marks[name]:raise RecoveryError('input changed during processing '+name)
            if complete and obj.hexdigest()!=m['object_sha256']:raise RecoveryError('exact V2 object digest mismatch')
        except (PauseRequested,KeyboardInterrupt):
            # An asynchronous signal can interrupt a multi-step hash/parser
            # update. Never overwrite the last consistent durable checkpoint.
            raise
        result={'result':'PASS-EXACT-BYTE-ACQUISITION' if complete else 'PAUSED','complete':complete,
            'offsets':dict(zip(NAMES,offsets)),'consumed_sha256':dict(zip(NAMES,[h.hexdigest() for h in hs])),
            'complete_object_sha256':obj.hexdigest() if complete else None,'complete_outer_profile_sha256':hs[0].hexdigest() if outer.stage=='done' and hs[0].hexdigest()==m['profile_sha256'] else None,
            'file_complete':{name:offsets[i]==m['files'][name]['bytes'] and hs[i].hexdigest()==m['files'][name]['sha256'] for i,name in enumerate(NAMES)},
            'outer_members':outer.members,'prefix_bytes_rechecked':replayed,'new_bytes':advanced,'seconds':time.monotonic()-started,
            'incremental_signature_verified':False,'signature_status':'UNAVAILABLE-BACKEND-ACCEPTANCE-REVIEW','profile_admitted':False,'source_authority_established':False}
        p.update(offsets=offsets,prefixes=[h.hexdigest() for h in hs],outer=outer.state(),object_prefix_sha256=obj.hexdigest(),sequence=p['sequence']+1,status=result['result'],result=result)
        atomic_save(checkpoint,p,key,fault=fault);emit('durable-checkpoint');return result
