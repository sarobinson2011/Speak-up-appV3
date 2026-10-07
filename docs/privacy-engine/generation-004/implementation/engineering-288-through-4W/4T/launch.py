#!/usr/bin/env python3
"""Explicit detached launch: survives ordinary terminal closure, no daemon service."""
import argparse,fcntl,json,os,subprocess,sys
from pathlib import Path
from run_task import ROOT,verify_package
p=argparse.ArgumentParser();p.add_argument('operation',choices=('run','resume'));p.add_argument('--task',type=Path,default=Path('/home/steve/dev/Engineering-288-execution/textual-4T'));p.add_argument('--authorize-review-hours',type=int);p.add_argument('--segment-ranks',type=int,choices=(16,32,64),default=64);a=p.parse_args();task=a.task.resolve()
verify_package()
if 'Speak-up-appV3' in task.parts or any(x.is_symlink() for x in [a.task,*a.task.parents]):raise ValueError('isolated unsymlinked task path required')
if not (task/'supervisor/IDENTITY.json').exists() and a.authorize_review_hours!=48:raise ValueError('explicit new textual 48-hour budget required')
task.mkdir(parents=True,exist_ok=True)
# The supervisor also locks; this check makes accidental duplicate launch clearer.
(task/'supervisor').mkdir(exist_ok=True)
with (task/'supervisor/LOCK').open('a+b') as lock:
 fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
cmd=[sys.executable,'-B',str(ROOT/'run_task.py'),a.operation,'--task',str(task),'--segment-ranks',str(a.segment_ranks)]
if a.authorize_review_hours is not None:cmd+=['--authorize-review-hours',str(a.authorize_review_hours)]
log=task/'terminal.log'
if log.exists() and log.stat().st_size>128*1024**2:
 previous=task/'terminal.previous.log'
 if previous.exists():previous.unlink()
 log.replace(previous)
with log.open('ab',buffering=0) as output:
 proc=subprocess.Popen(cmd,stdin=subprocess.DEVNULL,stdout=output,stderr=subprocess.STDOUT,start_new_session=True,close_fds=True)
print(json.dumps({'result':'TEXTUAL-SUPERVISOR-LAUNCHED','pid':proc.pid,'task':str(task),'log':str(log),'note':'Launch is not completion. Use status or read terminal.log. Closing this terminal does not stop the detached process.','actual_admission':False}))
