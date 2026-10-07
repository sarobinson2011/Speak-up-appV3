"""Standalone transport recovery. Semantic/qualification verdicts require collector."""
import argparse,json
from pathlib import Path
from .core import acquire
from integrated_auth.collector import implementation,Paused
from link_recovery.cli import read_key

def main():
 p=argparse.ArgumentParser();p.add_argument('input',type=Path);p.add_argument('--expectation',type=Path,required=True);p.add_argument('--state',type=Path,required=True);p.add_argument('--key',type=Path,required=True);p.add_argument('--rows',type=int);a=p.parse_args()
 try:
  e=json.loads(a.expectation.read_bytes());job={'independent_job':e['job'],'implementation':implementation()}
  if a.rows is not None and a.rows<=0:raise ValueError('positive row quantum')
  d=acquire(a.input,e['file'],e['kind'],e['binding'],a.state,read_key(a.key),job,stop_after=a.rows)
  print(json.dumps({'result':'COMPLETE-TRANSPORT-CATALOG','rows':len(d),'sha256':e['file']['sha256'],'model_membership_established':False,'authentication_success':False,'profile_admitted':False}));return 0
 except Paused:print(json.dumps({'result':'PAUSED','authentication_success':False,'profile_admitted':False}));return 3
 except Exception as e:print(json.dumps({'result':'REJECTED','detail':str(e),'authentication_success':False,'profile_admitted':False}));return 2
if __name__=='__main__':raise SystemExit(main())
