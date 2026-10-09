"""Explicit, resumable local supervisor binding transition; not source authentication."""
import argparse,copy
from superlib import *
OLD_NAMES=['superlib.py','worker.py','supervisor.py','launch.py','probe.py','probe_worker.py','host.py']
OLD_MANIFEST_SHA='5264f04310fba2aa1fa843de88821980b6cc5d1a2b9739d0e244ca2fd9f5170d'
TRANSITION='DIAGNOSTIC-1-TRANSITION'

def migrate(task,old_kit,fault=None):
 t=Path(task).resolve();oldroot=Path(old_kit).resolve()
 need(t.is_dir() and oldroot!=ROOT,'existing task and separate original kit required')
 key=core.keyread(t/'execution.key')
 with Lock(t/'CONTROL.LOCK'):
  original=ROOT/'ORIGINAL-PACKAGE-MANIFEST.json'
  need(core.sha(original)==OLD_MANIFEST_SHA,'original manifest binding')
  m=json.loads(original.read_bytes())
  for x in m['files']:
   p=oldroot/x['path'];need(not p.is_symlink() and p.is_file() and p.stat().st_size==x['bytes'] and core.sha(p)==x['sha256'],'original kit mutation: '+x['path'])
  newbinding=binding();expected_old={'code':{n:core.sha(oldroot/n) for n in OLD_NAMES},'runtime':newbinding['runtime'],'package_path':str(oldroot),'platform':newbinding['platform']}
  # Check all eight actual runtime inputs in both kits; the validator's identity is unchanged.
  for name,h in newbinding['runtime']['files'].items():need(core.sha(oldroot/'runtime'/name)==h,'changed validator/emitter: '+name)
  transition=t/TRANSITION;planfile=transition/'PLAN.json'
  if not planfile.exists():
   need(not transition.exists(),'incomplete unpublished transition directory; preserve and inspect')
   c=read(t/'CONFIG.json',key);b=read(t/'BUDGET.json',key)
   need(c['task']==str(t) and c['implementation']==expected_old,'original task/code binding')
   need(b['config_sha256']==hashlib.sha256(core.wire(c)).hexdigest() and b['lease'] is None,'budget must be bound and quiescent')
   need((t/'data/STATE.json').exists(),'saved validator state required')
   with core.Job(t/'data',t/'execution.key') as job:
    need(job.identity['manifest']==c['manifest'],'source/collector correspondence')
    offset=job.state['offset'];need(job.state['status']!='REJECTED','terminal rejection cannot migrate to success')
   fingerprints={n:core.sha(t/'data'/n) for n in ['IDENTITY.json','STATE.json','spool.bin'] if (t/'data'/n).exists()}
   nc=copy.deepcopy(c);nc['implementation']=newbinding
   nb=copy.deepcopy(b);nb['config_sha256']=hashlib.sha256(core.wire(nc)).hexdigest();nb['sequence']+=1
   plan={'format':'CP4W-DIAGNOSTIC-MIGRATION-1','task':str(t),'old_kit':str(oldroot),'new_kit':str(ROOT),'old_config':c,'old_budget':b,'new_config':nc,'new_budget':nb,'data_sha256':fingerprints,'offset':offset,'trust':'Explicit user-authorized local implementation transition; no qualification','actual_admission':False}
   # Single sealed plan publication: no multi-file dependency before this durable record.
   tmp=t/(TRANSITION+'.preparing')
   if tmp.exists():
    need(set(x.name for x in tmp.iterdir())<= {'PLAN.json','PLAN.json.part'},'unexpected preparation content')
    shutil.rmtree(tmp)
   tmp.mkdir(mode=0o700);save(tmp/'PLAN.json',plan,key);core.fsyncdir(tmp);os.replace(tmp,transition);core.fsyncdir(t)
   if fault:fault('plan')
  plan=read(planfile,key)
  need(plan['task']==str(t) and plan['old_kit']==str(oldroot) and plan['new_kit']==str(ROOT),'cross-job transition')
  need(plan['old_config']['implementation']==expected_old and plan['new_config']['implementation']==newbinding,'stale transition implementation')
  if (transition/'COMPLETE.json').exists():
   complete=read(transition/'COMPLETE.json',key)
   c=read(t/'CONFIG.json',key);b=budget(t,key,c)
   need(c==plan['new_config'] and complete['plan_sha256']==core.sha(planfile),'completed transition substitution')
   need(b['charged_ns']>=plan['old_budget']['charged_ns'] and b['authorized_ns']>=plan['old_budget']['authorized_ns'],'budget rollback')
   return {'result':'ALREADY-MIGRATED','offset_at_migration':plan['offset'],'actual_admission':False}
  currentc=read(t/'CONFIG.json',key);currentb=read(t/'BUDGET.json',key)
  need(currentc in [plan['old_config'],plan['new_config']] and currentb in [plan['old_budget'],plan['new_budget']],'unexpected state during transition')
  need(currentb['lease'] is None,'active attempt')
  actual={n:core.sha(t/'data'/n) for n in ['IDENTITY.json','STATE.json','spool.bin'] if (t/'data'/n).exists()}
  need(actual==plan['data_sha256'],'validator state changed during transition')
  # Reject input mutations even when finishing an interrupted publication.
  with core.Job(t/'data',t/'execution.key') as job:need(job.identity['manifest']==plan['new_config']['manifest'],'source correspondence')
  save(t/'CONFIG.json',plan['new_config'],key)
  if fault:fault('config')
  save(t/'BUDGET.json',plan['new_budget'],key)
  if fault:fault('budget')
  need(actual=={n:core.sha(t/'data'/n) for n in actual},'validator bytes changed')
  save(transition/'COMPLETE.json',{'plan_sha256':core.sha(planfile),'offset':plan['offset'],'actual_admission':False},key)
  return {'result':'PASS-MIGRATED-NOT-STARTED','offset':plan['offset'],'charged_seconds':plan['new_budget']['charged_ns']/NS,'authorized_seconds':plan['new_budget']['authorized_ns']/NS,'validator_state_bytes_unchanged':True,'runtime_identity_unchanged':True,'old_backup_binding_preserved':True,'actual_admission':False}
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--task',required=True);p.add_argument('--old-kit',required=True);a=p.parse_args()
 try:print(json.dumps(migrate(a.task,a.old_kit),indent=2))
 except BaseException as e:print(json.dumps({'result':'BLOCKED','error':type(e).__name__+': '+str(e),'actual_admission':False}));sys.exit(2)
