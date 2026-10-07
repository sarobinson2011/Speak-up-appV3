import argparse,json,signal
from pathlib import Path
from .core import execute
from .integration import run
from link_recovery.cli import create_key,RecoveryError,PauseRequested

def main():
    p=argparse.ArgumentParser();p.add_argument('operation',choices=('keygen','start','resume','integrate','continue'));p.add_argument('--job',type=Path);p.add_argument('--key',required=True,type=Path);p.add_argument('--checkpoint',type=Path);p.add_argument('--new-bytes',type=int,default=64*1024*1024);p.add_argument('--seconds',type=float,default=50);p.add_argument('--chunk-bytes',type=int,default=65536);p.add_argument('--appointment',type=Path);a=p.parse_args()
    if a.operation=='keygen':create_key(a.key);return 0
    if not a.job or not a.checkpoint:p.error('--job and --checkpoint required')
    def stop(*_):raise PauseRequested()
    signal.signal(signal.SIGTERM,stop)
    import sys
    def progress(x):print(json.dumps(x),file=sys.stderr,flush=True)
    try:
        kw=dict(resume=a.operation in ('resume','continue'),new_bytes=a.new_bytes,seconds=a.seconds,chunk_bytes=a.chunk_bytes,progress=progress)
        if a.operation in ('integrate','continue'):r=run(a.job,a.checkpoint,a.key,appointment_value=json.loads(a.appointment.read_bytes()) if a.appointment else None,**kw)
        else:r=execute(a.job,a.checkpoint,a.key,**kw)
    except (ValueError,OSError,RecoveryError,PauseRequested,KeyboardInterrupt) as e:
        r={'result':'REJECTED-OR-INTERRUPTED','detail':str(e) or 'interrupted; resume last durable journal','complete_object_sha256':None,'profile_admitted':False,'incremental_signature_verified':False}
    print(json.dumps(r,indent=2));return 3 if r['result']=='PAUSED' else 0 if r['result']=='PASS-EXACT-BYTE-ACQUISITION' else 2
if __name__=='__main__':raise SystemExit(main())
