"""CP4H file-backed three-scope/ledger integration with authenticated local recovery.

Replay, not receipt assertions, restores parser and digest states. Journals do not
appoint authorities. Every call reruns the source-grounded ordered collector.
"""
import hashlib,hmac,json,time,fcntl,os,tempfile,math
from pathlib import Path
from v4_ingest.records import parse,canonical,digest,require,primitive,profile_identity,ValidationError
from v4_ingest.wire import FILES,EVIDENCE_HEADER,read_table,signature_line
from admission_kernel.admission import collect
from admission_kernel.failures import ORDER,Failures
from large_auth.core import execute
from pure_auth.controller import verify_job,identity
from link_recovery.cli import atomic_save,read_key,RecoveryError
from link_stream.validator import State,ModelIndex
from .adapters import small,chunks,SourceMap,TokenMatcher,CAP
ROOT=Path(__file__).resolve().parents[1]
VERSION='CP4P-FILE-COLLECTOR-1'
SCOPES=('ROOT-ELIGIBLE','SCOPED-USED','NOT-APPLICABLE')

class Paused(ValidationError):
    def __init__(self):super().__init__('stage paused; no complete assertion',category='INCOMPLETE-EVIDENCE-UNIVERSE')

def implementation():
    dirs=('integrated_auth','admission_kernel','scope_auth','ledger_kernel','v4_ingest','large_auth','pure_auth','link_stream','semantic_stream','recovery_schedule','link_recovery','occurrence_values','metadata_catalog')
    return {'native':__import__('link_recovery.cli',fromlist=['validator_identity']).validator_identity(),'backend':identity(),'files':{str(p.relative_to(ROOT)):digest(p.read_bytes()) for d in dirs for p in sorted((ROOT/d).rglob('*.py'))},'accepted_schema':digest((ROOT/'v4_ingest/data/security-fields.tsv').read_bytes())}

def journal(path,key,binding):
    if not path.exists():return {'format':VERSION,'binding':binding,'sequence':0,'stages':{},'last_result':None}
    with path.open('rb') as stream:raw=stream.read(1024*1024+1)
    require(len(raw)<=1024*1024,'collector journal cap')
    x=json.loads(raw);require(isinstance(x,dict) and set(x)=={'payload','hmac_sha256'},'corrupt collector journal envelope');p=x['payload'];expected=hmac.new(key,canonical(p).rstrip(b'\n'),hashlib.sha256).hexdigest()
    # atomic_save uses sorted compact ensure_ascii JSON WITHOUT terminal LF.
    require(hmac.compare_digest(expected,x['hmac_sha256']),'corrupt collector journal')
    require(p['format']==VERSION and p['binding']==binding,'stale/substituted/incompatible collector receipt')
    return p

class Adapter:
    def __init__(self,m,base,ck,key_path,p,key,new_bytes,seconds,chunk,progress):
        self.m,self.base,self.ck,self.key_path,self.p,self.key=m,base,ck,key_path,p,key
        self.new_bytes,self.seconds,self.chunk,self.progress=new_bytes,seconds,chunk,progress
        self.paused=False;self.jobs={};self.status={};self.deadline=time.monotonic()+seconds
        from semantic_stream.storage import ACTIVE
        self.store=ACTIVE.get();self.store.tick=self.remaining;self.acquired=__import__('semantic_stream.lifetime',fromlist=['ByteLRU']).ByteLRU();self.providers=[];self.acquisition_count=0;self.new_snapshots=0
        from metadata_catalog.core import temporary
        self.acquisition_seen=temporary(self.store.root,'acquisition-seen-');self.store.docs.append(self.acquisition_seen)
        from recovery_schedule.state import ACTIVE as SCHEDULE
        self.scheduler=SCHEDULE.get()
    def remaining(self):
        r=self.deadline-time.monotonic()
        if r<=.01:self.paused=True;raise Paused()
        return r
    def save(self):self.p['sequence']+=1;atomic_save(self.ck,self.p,self.key)
    def blob(self,e):
        from semantic_stream.storage import Blob
        key=(e['path'],e['bytes'],e['sha256'])
        seen_key=hashlib.sha256(json.dumps(key).encode()).hexdigest()
        if seen_key not in self.acquisition_seen:self.acquisition_seen[seen_key]=True;self.acquisition_count+=1
        if key in self.acquired:return self.acquired[key]
        if self.scheduler is not None:
            label='acquisition:'+e['path'];old=self.scheduler.read(label)
            if old is not None:
                require(old['inputs']==e and old['complete'],'stale/incomplete acquisition receipt')
                source=(self.base/e['path']).resolve();path=self.scheduler.root/old['result']['snapshot']
                require(path.parent==self.scheduler.root and set(old['artifacts'])=={str(path)},'snapshot containment')
                self.scheduler.verify(source,e['sha256'],force=True);self.scheduler.verify(path,e['sha256'],force=True)
                result=Blob(self.store,path);self.acquired[key]=result;self.scheduler.event(label,'REUSED-EXACT-SNAPSHOT');return result
        path=self.store.path('acquired');self.new_snapshots+=1
        with path.open('wb') as stream:
            class Sink:
                def feed(self,b):stream.write(b)
            self.replay('semantic:'+e['path'],e,Sink(),stream.flush)
        if self.scheduler is not None:
            import shutil
            target=self.scheduler.root/(self.scheduler.name(label)+'.blob');tmp=target.with_suffix('.part');shutil.copyfile(path,tmp)
            with tmp.open('rb') as stream:os.fsync(stream.fileno())
            os.replace(tmp,target)
            from link_recovery.cli import fsync_dir
            fsync_dir(target.parent)
            self.scheduler.save(label,e,{'snapshot':target.name},True,artifacts={str(target):e['sha256']});path=target
        result=Blob(self.store,path);self.acquired[key]=result;return result
    def octets(self,name):return self.blob(self.m['records'][name])
    def provider(self,trusted,materials,sources):
        from semantic_stream.provider import StreamingProvider
        p=StreamingProvider(trusted,materials,sources,self.store);self.providers.append(p);return p
    def auth_budget(self):
        return self.scheduler.auth_new_bytes if self.scheduler is not None and self.scheduler.auth_new_bytes is not None else self.new_bytes
    def security_digest(self):return digest(self.octets('security_records_hex'))
    def source_map(self,name):
        from collections.abc import Mapping
        adapter=self;entries=self.m[name]
        class Sources(Mapping):
            def __len__(self):return len(entries)
            def __iter__(self):return iter(entries)
            def __getitem__(self,k):
                e=entries[k];require(k==e['sha256'],'source directory key identity',category='INVALID-EVIDENCE-DIGEST');return adapter.blob(e)
        return Sources()
    def file_identities(self,scope):return {n:{k:e[k] for k in ('bytes','sha256')} for n,e in self.m['bundles'][scope]['files'].items()}
    def authenticate(self,scope,appointed,f):
        report={'four_file_identity':False,'signature_valid':False,'complete':False,'source_authority_established':False,'profile_admitted':False,'backend':identity()['binary_sha256']}
        item=self.m['bundles'][scope];files=item['files'];job=self.ck.parent/(self.ck.name+'.'+scope+'.job.json')
        j={'format':'CP4F-EXACT-BYTE-JOB-1','files':{'outer':self.m['records']['outer_hex'],**files},'object_sha256':item['object_sha256'],'profile_sha256':self.m['request']['profile_digest'],'model':self.m['model'],'contract':self.m['contract'],'scope':scope,'phase':self.m['request']['phase'],'canonical_model_sha256':self.m['canonical_model_sha256']}
        # Job paths remain contained under the INPUT directory. Journals live elsewhere.
        job=self.base/('.4h-'+scope+'.job.json');raw=canonical(j)
        if job.exists():require(job.read_bytes()==raw,'stale generated acquisition job')
        else:
            fd,tmp=tempfile.mkstemp(prefix='.job-',dir=self.base)
            try:
                with os.fdopen(fd,'wb') as stream:stream.write(raw);stream.flush();os.fsync(stream.fileno())
                os.replace(tmp,job)
                from link_recovery.cli import fsync_dir
                fsync_dir(self.base)
            finally:Path(tmp).unlink(missing_ok=True)
        self.jobs[scope]=j
        def failure(code,e):f.add(code,scope+': '+str(e))
        bc=Path(str(self.ck)+'.'+scope+'.bytes')
        try:
            fn=lambda:execute(job,bc,self.key_path,resume=bc.exists(),new_bytes=self.auth_budget(),seconds=self.remaining(),chunk_bytes=self.chunk,progress=self.progress)
            r=self.stage('four-file:'+scope,j,fn,lambda r:r['complete'])
            report['byte_stage']=r;report['four_file_identity']=r['complete']
            if not r['complete']:self.paused=True
        except Paused:pass
        except (ValueError,OSError,RecoveryError) as e:failure('MISSING-EVIDENCE' if isinstance(e,OSError) else 'PROFILE-DIGEST-MISMATCH' if 'outer' in str(e) and 'digest' in str(e) else 'INVALID-EVIDENCE-DIGEST',e)
        if appointed is None:failure('INVALID-EVIDENCE-AUTHORITY','independent appointment unavailable')
        else:
            cc=Path(str(self.ck)+'.'+scope+'.crypto')
            try:
                issuer,_=signature_line(small(self.base,files['signature.txt'],4096))
                require(issuer==appointed['authority_id'],'signature appointed issuer')
                fn=lambda:verify_job(job,cc,self.key_path,bytes.fromhex(appointed['public_key']),resume=cc.exists(),new_bytes=self.auth_budget(),seconds=self.remaining(),chunk_bytes=self.chunk,progress=self.progress)
                r=self.stage('pure-ed25519:'+scope,j,fn,lambda r:r['cryptographic_signature_verified'],appointed)
                report['crypto_stage']=r;report['signature_valid']=r['cryptographic_signature_verified']
                if not report['signature_valid']:self.paused=True
            except Paused:pass
            except (ValueError,OSError,RecoveryError) as e:failure('MISSING-EVIDENCE' if isinstance(e,OSError) else 'INVALID-EVIDENCE-AUTHENTICATION',e)
        report['complete']=report['four_file_identity'] and report['signature_valid']
        return files,report
    def stage(self,label,job,fn,done,authority=None):
        if self.scheduler is None:return fn()
        entries=list(job['files'].values())+[job['model'],job['contract']]
        inputs={'files':{str((self.base/e['path']).resolve()):e['sha256'] for e in entries},'job':job,'appointment':authority}
        suffix='.bytes' if label.startswith('four-file:') else '.crypto'
        path=Path(str(self.ck)+'.'+label.split(':',1)[1]+suffix)
        return self.scheduler.cached(label,inputs,fn,done,outputs=lambda:{str(path):__import__('recovery_schedule.state',fromlist=['sha']).sha(path)})
    def tables(self,scope,files):
        rows=read_table(small(self.base,files['evidence.tsv'],1024*1024),EVIDENCE_HEADER);require(len(rows)==1,'sole evidence row');r=rows[0]
        for k,v in r.items():
            if k.endswith('sha256'):primitive('DIGEST',v)
            elif k.endswith('result'):require(v in ('PASS','FAIL'),'signed result enum')
            elif k=='algorithm':require(v=='ED25519-RFC8032','pure signature algorithm')
            elif k=='evidence_kind':require(v in ('ADMISSION-COMPONENT','ADMISSION-COMPOSITION','COMPONENT','COMPOSITION'),'evidence kind')
            else:primitive('ID',v)
        profile_identity(r['profile_id']);composition=r['evidence_kind'].endswith('COMPOSITION')
        require((r['component_id']=='NOT-APPLICABLE')==composition,'component/kind join')
        scopeid=r['profile_id']+('#ADMISSION-V1' if r['evidence_kind'].startswith('ADMISSION-') else '#OCCURRENCE-SET-'+files['tokens.tsv']['sha256'])
        require(r['scope_id']==scopeid and r['evidence_id']==r['profile_id']+'#'+r['evidence_kind']+'-'+('ALL' if composition else r['component_id']),'evidence identity constructors',category='INVALID-ACTION-CONTEXT')
        issuer,_=signature_line(small(self.base,files['signature.txt'],4096));require(issuer==r['issued_by'],'signature evidence issuer',category='INVALID-EVIDENCE-AUTHENTICATION')
        for n in ('tokens','links'):require(r[n+'_sha256']==files[n+'.tsv']['sha256'],'signed file identity',category='INVALID-EVIDENCE-DIGEST')
        return {'evidence':r,'object_sha256':self.m['bundles'][scope]['object_sha256']}
    def replay(self,label,e,parser,finish):
        old=self.p['stages'].get(label,{'offset':0,'prefix_sha256':digest(b'')})
        if self.scheduler is not None:
            saved=self.scheduler.read('replay:'+label)
            if saved is not None:
                require(saved['inputs']==e,'changed replay input');old=saved['result']
        limit=old['offset']+self.new_bytes
        h=hashlib.sha256();count=0;verified=old['offset']==0;last=time.monotonic()
        # Feed every consumed byte again: parser/order/count state is reconstructed
        # from exact input prefix; no caller-provided state or PASS is imported.
        for block in chunks(self.base,e,self.chunk):
            off=0
            while off<len(block):
                self.remaining()
                boundary=old['offset'] if count<old['offset'] else limit
                n=min(len(block)-off,boundary-count);b=block[off:off+n]
                h.update(b);parser.feed(b);count+=n;off+=n
                if self.progress and time.monotonic()-last>=1:
                    self.progress({'stage':label,'consumed':count,'replay_target':old['offset'],'total':e['bytes']});last=time.monotonic()
                if count==old['offset']:
                    require(h.hexdigest()==old['prefix_sha256'],'changed consumed stage prefix',category='INVALID-EVIDENCE-DIGEST');verified=True
                if count==limit and count<e['bytes']:
                    require(verified,'unverified recovery prefix');self.save_replay(label,e,{'offset':count,'prefix_sha256':h.hexdigest(),'complete':False});self.paused=True;raise Paused()
        require(verified,'truncated recovery prefix',category='INVALID-EVIDENCE-DIGEST');finish()
        self.save_replay(label,e,{'offset':count,'prefix_sha256':h.hexdigest(),'complete':True})
        return {'complete':True,'bytes_consumed':count,'complete_stream_sha256':h.hexdigest(),'replayed_bytes':old['offset']}
    def save_replay(self,label,e,state):
        if self.scheduler is not None:self.scheduler.save('replay:'+label,e,state,state['complete'])
        else:self.p['stages'][label]=state;self.save()
    def scoped_files(self,scope,scoped,request,values,parsed):
        files=self.m['bundles'][scope]['files'];failures=[];result=None
        token=TokenMatcher(scoped,request['phase'],values)
        try:self.replay(scope+'.tokens',files['tokens.tsv'],token,token.finish)
        except (ValueError,OSError) as e:failures.append(e)
        if self.scheduler is not None:
            from recovery_schedule.native import validate
            try:result=validate(self,scope,scoped,request,values)
            except (ValueError,OSError,RecoveryError) as e:failures.append(e)
            if failures:
                self.status[scope]=[{'code':getattr(e,'category','MISSING-EVIDENCE'),'detail':str(e)} for e in failures];raise failures[0]
            return result
        state=State(ModelIndex(scoped,request['phase'],values))
        class Parser:
            def __init__(self):self.pending=bytearray()
            def feed(self,b):
                start=0
                while start<len(b):
                    end=b.find(b'\n',start);end=len(b) if end<0 else end
                    require(len(self.pending)+end-start<=state.index.max_line,'maximum legal row size')
                    self.pending.extend(b[start:end])
                    if end==len(b):break
                    state.line(bytes(self.pending));self.pending.clear();start=end+1
            def finish(self):require(not self.pending,'terminal LF');state.finish()
        parser=Parser()
        try:
            result=self.replay(scope+'.links',files['links.tsv'],parser,parser.finish)
            result.update(structural_rows=state.structural,potential_rows=state.potential)
        except (ValueError,OSError) as e:failures.append(e)
        if failures:
            # Preserve separately discoverable token/link categories in outer wrapper.
            self.status[scope]=[{'code':getattr(e,'category','MISSING-EVIDENCE'),'detail':str(e)} for e in failures]
            raise failures[0]
        return result

def _run(manifest,trusted_path,checkpoint,key_path,*,resume=False,new_bytes=64*1024*1024,seconds=50,chunk_bytes=65536,progress=None):
    manifest=Path(manifest).resolve();base=manifest.parent;ck=Path(checkpoint).resolve();ck.parent.mkdir(parents=True,exist_ok=True)
    require(0<new_bytes and 0<seconds and math.isfinite(seconds) and 0<chunk_bytes<=1024*1024,'bounded execution options')
    with manifest.open('rb') as stream:raw=stream.read(16*1024*1024+1)
    require(len(raw)<=16*1024*1024,'carrier capability limit',category='INCOMPLETE-EVIDENCE-UNIVERSE');m=parse(raw)
    require(m['format']==VERSION,'file collector carrier')
    from semantic_stream.storage import ACTIVE
    def trusted_chunks():
        with Path(trusted_path).open('rb') as stream:
            while b:=stream.read(65536):yield b
    trustedraw=ACTIVE.get().write(trusted_chunks());trusted=parse(trustedraw)
    binding={'manifest_path':str(manifest),'manifest_sha256':digest(raw),'trusted_path':str(Path(trusted_path).resolve()),'trusted_sha256':digest(trustedraw),'implementation':implementation()}
    key=read_key(key_path)
    with open(str(ck)+'.lock','a+b') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        require(resume or not ck.exists(),'existing journal requires resume');require(not resume or ck.exists(),'resume journal missing')
        p=journal(ck,key,binding)
        from metadata_catalog.adapters import hydrate
        handles=[]
        def catalog_tick():
            if time.monotonic()>=catalog_deadline:raise Paused()
        catalog_deadline=time.monotonic()+seconds
        m,trusted,catalog_errors=hydrate(m,trusted,base,Path(str(ck)+'.catalogs'),key,binding,handles,catalog_tick)
        ACTIVE.get().docs.extend(handles)
        a=Adapter(m,base,ck,key_path,p,key,new_bytes,seconds,chunk_bytes,progress)
        # Independently acquired canonical model and selected contract joins. A job
        # descriptor alone does not establish either correspondence.
        f=Failures()
        for error in catalog_errors:f.add(getattr(error,'category','MISSING-EVIDENCE'),str(error))
        for name,expected in [('model',trusted.get('model')),('contract',trusted.get('evidence_contract'))]:
            try:require(parse(a.blob(m[name]))==expected,'exact source-owned '+name+' correspondence',category='INVALID-ACTION-CONTEXT')
            except (ValueError,OSError) as e:f.add(getattr(e,'category','MISSING-EVIDENCE'),str(e))
        if m['canonical_model_sha256']!=digest(canonical(trusted.get('model'))):f.add('INVALID-ACTION-CONTEXT','canonical model join')
        result=collect(m['request'],trusted,adapter=a)
        for code,reasons in result['reasons'].items():
            for reason in reasons:f.add(code,reason)
        for errors in a.status.values():
            for e in errors:f.add(e['code'] if e['code'] in ORDER else 'INVALID-PROFILE-SCHEMA',e['detail'])
        out=f.result(m['request']['mode'],result['bindings'])
        out['semantic_acquisition']={'exact_files':a.acquisition_count,'new_snapshots':a.new_snapshots,'temporary_bytes_at_completion':sum(p.stat().st_size for p in a.store.root.iterdir() if p.is_file()),'invocations':[i for p in a.providers for i in p.invocation_receipts],'invocation_count':sum(p.invocation_receipts.total for p in a.providers),'invocation_diagnostic_tail_limit_per_provider':32,'invocation_diagnostic_peak_bytes':max((p.invocation_receipts.cache.peak for p in a.providers),default=0),'qualification_established':False,'recovery':'FULL-PREFIX-REACQUISITION-AND-REINDEX'}
        out['semantic_acquisition']['lifetime']={**a.store.metrics(),'acquisition_cache_peak_bytes':a.acquired.peak,'acquisition_cache_limit_bytes':a.acquired.limit,'acquisition_cache_evictions':a.acquired.evictions}
        out['occurrence_acquisition']=getattr(a,'occurrence_report',None)
        out['processing_complete']=not a.paused;out['pending_stages']=a.paused
        if a.paused:out['result']='PAUSED';out['bindings']={};out['complete_authentication']=False
        if f.reasons and out['bindings']:
            # New adapter failures must also suppress positive ledger verdicts.
            out['bindings']['computed_dispositions']={k:'NOT-ESTABLISHED' for k in out['bindings'].get('computed_dispositions',{})};out['bindings']['computed_budgets']={}
            if 'scope_validation' in out['bindings']:
                sv=out['bindings']['scope_validation'];sv['conditional_checks_pass']=False;sv['ready']=False;sv['qualification']='NOT-ESTABLISHED'
                for scope in sv.get('scopes',{}).values():scope['ready']=False;scope['qualification']='NOT-ESTABLISHED'
        p['last_result']={'result':out['result'],'earliest_failure':out['earliest_failure'],'failures':out['failures'],'processing_complete':out['processing_complete']};a.save()
        return out


def run(*args,**kwargs):
    from semantic_stream.storage import Store,ACTIVE
    store=Store();token=ACTIVE.set(store)
    result=None
    try:
        result=_run(*args,**kwargs);return result
    finally:
        ACTIVE.reset(token);store.close()
        if result is not None:result['semantic_acquisition']['cleanup']={'store_closed':store.closed,'open_index_connections':len(store.pool.data),'temporary_root_removed':not store.root.exists()}
