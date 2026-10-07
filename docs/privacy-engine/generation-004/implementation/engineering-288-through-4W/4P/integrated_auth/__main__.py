import argparse,json,sys,signal
from pathlib import Path
from recovery_schedule.runner import run
from integrated_auth.collector import Paused
from link_recovery.cli import create_key,PauseRequested

def main():
    p=argparse.ArgumentParser(description='Conditional file-backed collector; actual admission always disabled')
    p.add_argument('operation',choices=('keygen','start','resume'));p.add_argument('--key',required=True,type=Path)
    p.add_argument('--manifest',type=Path);p.add_argument('--trusted',type=Path);p.add_argument('--checkpoint',type=Path)
    p.add_argument('--new-bytes',type=int,default=67108864);p.add_argument('--seconds',type=float,default=50);p.add_argument('--chunk-bytes',type=int,default=65536)
    p.add_argument('--quanta',type=int,default=1);p.add_argument('--auth-new-bytes',type=int)
    a=p.parse_args()
    if a.operation=='keygen':create_key(a.key);return 0
    def interrupt(*args):raise PauseRequested()
    signal.signal(signal.SIGTERM,interrupt);signal.signal(signal.SIGINT,interrupt)
    try:
        r=run(a.manifest,a.trusted,a.checkpoint,a.key,resume=a.operation=='resume',new_bytes=a.new_bytes,seconds=a.seconds,chunk_bytes=a.chunk_bytes,quanta=a.quanta,auth_new_bytes=a.auth_new_bytes,progress=lambda x:print(json.dumps(x),file=sys.stderr))
        print(json.dumps(r,indent=2));return 3 if r['result']=='PAUSED' else 0 if not r['failures'] else 2
    except (PauseRequested,Paused):print(json.dumps({'result':'INTERRUPTED','profile_admitted':False,'authentication_success':False}));return 3
    except Exception as e:print(json.dumps({'result':'REJECTED','detail':str(e),'profile_admitted':False,'authentication_success':False}));return 2
if __name__=='__main__':raise SystemExit(main())
