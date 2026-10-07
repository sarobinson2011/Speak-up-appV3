import argparse,json,signal,sys,subprocess
from pathlib import Path
from .controller import verify_job
from .preflight import run
from link_recovery.cli import create_key,RecoveryError,PauseRequested

def main():
    p=argparse.ArgumentParser();p.add_argument('operation',choices=('keygen','start','resume','preflight','continue'));p.add_argument('--job',type=Path);p.add_argument('--checkpoint',type=Path);p.add_argument('--key',required=True,type=Path);p.add_argument('--public-key');p.add_argument('--new-bytes',type=int,default=64*1024*1024);p.add_argument('--seconds',type=float,default=50);p.add_argument('--chunk-bytes',type=int,default=65536);a=p.parse_args()
    if a.operation=='keygen':create_key(a.key);return 0
    if not a.job or not a.checkpoint or not a.public_key:p.error('--job, --checkpoint and --public-key required')
    def stop(*_):raise PauseRequested()
    signal.signal(signal.SIGTERM,stop)
    try:
        fn=run if a.operation in ('preflight','continue') else verify_job
        r=fn(a.job,a.checkpoint,a.key,bytes.fromhex(a.public_key),resume=a.operation in ('resume','continue'),new_bytes=a.new_bytes,seconds=a.seconds,chunk_bytes=a.chunk_bytes,progress=lambda x:print(json.dumps(x),file=sys.stderr,flush=True))
    except (ValueError,OSError,RecoveryError,PauseRequested,KeyboardInterrupt,subprocess.SubprocessError) as e:
        r={'result':'REJECTED-OR-INTERRUPTED','detail':str(e) or 'interrupted; last durable journal unchanged','cryptographic_signature_verified':False,'profile_admitted':False}
    print(json.dumps(r,indent=2));return 3 if r['result']=='PAUSED' else 0 if r.get('cryptographic_signature_verified') is True else 2
if __name__=='__main__':raise SystemExit(main())
