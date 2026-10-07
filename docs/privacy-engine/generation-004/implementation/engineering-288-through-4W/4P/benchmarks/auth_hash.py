"""One <=60s synthetic byte-acquisition benchmark; no universe or link semantics."""
import hashlib,json,resource,subprocess,sys,tempfile,time
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1];sys.path.insert(0,str(ROOT))
from fixtures.auth_jobs import make
from fixtures.construct import wire
from large_auth.core import execute
from link_recovery.cli import create_key

def child():
    began=time.monotonic()
    with tempfile.TemporaryDirectory(prefix='cp4f-synthetic-') as d:
        root=Path(d);job=make(root/'input');m=json.loads(job.read_bytes());p=job.parent/'links.tsv'
        block=bytes(range(256))*4096;h=hashlib.sha256()
        with p.open('wb') as f:
            for _ in range(96):f.write(block);h.update(block)
        m['files']['links.tsv'].update(bytes=p.stat().st_size,sha256=h.hexdigest())
        # Independent exact object serializer/oracle, bounded 128 KiB reads.
        h=hashlib.sha256(b'PE-TSE-PRIVACY-EVIDENCE-OBJECT-V2\n')
        for name in ('evidence.tsv','tokens.tsv','links.tsv','signature.txt'):
            path=job.parent/name;h.update(path.stat().st_size.to_bytes(8,'big'))
            with path.open('rb') as f:
                while b:=f.read(131072):h.update(b)
        m['object_sha256']=h.hexdigest();job.write_bytes(wire(m));key=root/'key';create_key(key)
        rows=[]
        def go(name,n,resume=False):
            start=time.monotonic();r=execute(job,root/name,key,new_bytes=n,seconds=45,chunk_bytes=1048576,resume=resume)
            rows.append({'operation':name+('-resume' if resume else '-start'),'wall_seconds':time.monotonic()-start,'result':r});return r
        full=go('uninterrupted',128*1048576);part=go('recovered',40*1048576);resumed=go('recovered',128*1048576,True)
        assert not part['complete'] and full['complete'] and resumed['complete']
        assert full['complete_object_sha256']==resumed['complete_object_sha256']==m['object_sha256']
        assert full['consumed_sha256']==resumed['consumed_sha256']
        total=sum(e['bytes'] for e in m['files'].values());signed=25+sum(m['files'][n]['bytes'] for n in ('evidence.tsv','tokens.tsv','links.tsv'))
        return {'result':'PASS','synthetic_payload_bytes':96*1048576,'exact_signed_message_bytes':signed,'input_acquisition_bytes':total,'object_sha256':m['object_sha256'],'rows':rows,'elapsed_seconds':time.monotonic()-began,'max_rss_kib':resource.getrusage(resource.RUSAGE_SELF).ru_maxrss,'chunk_limit_bytes':1048576,'temporary_disk_bytes':sum(p.stat().st_size for p in root.rglob('*') if p.is_file()),'benchmark_only':True,'large_signature_verified':False,'full_retained_stream_processed':False,'profile_admitted':False}
if __name__=='__main__':
    if '--child' in sys.argv:print(json.dumps(child(),indent=2))
    else:
        began=time.monotonic()
        try:
            run=subprocess.run([sys.executable,str(Path(__file__).resolve()),'--child'],cwd=ROOT,capture_output=True,text=True,timeout=60)
            r=json.loads(run.stdout) if run.returncode==0 else {'result':'FAIL','stderr':run.stderr}
        except subprocess.TimeoutExpired:r={'result':'TIMEOUT','benchmark_only':True}
        r['hard_limit_seconds']=60;r['aggregate_benchmark_seconds']=time.monotonic()-began
        target=Path(sys.argv[1]) if len(sys.argv)>1 else ROOT/'results/4F-benchmark.json';target.write_text(json.dumps(r,indent=2)+'\n');print(json.dumps(r,indent=2));sys.exit(0 if r['result']=='PASS' else 1)
