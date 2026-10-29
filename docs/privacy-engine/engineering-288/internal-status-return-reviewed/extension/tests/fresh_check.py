"""Fresh public/semantic/derivation checks for this extension only."""
import copy,json,runpy,sys,time,types,traceback
from pathlib import Path
r=Path(sys.argv[1]).resolve();runpy.run_path(str(r/'tests/guard.py'))['install'](r)
p=r/'code/correspondence.py';m=types.ModuleType('_status_fresh');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
start=time.monotonic();checks=[]
def check(name,fn):
 result=fn();assert result is not False,name;checks.append({'check':name,'result':'PASS'});print('PASS '+name,flush=True);return result
def reject(fn):
 try:fn()
 except ValueError:return True
 raise AssertionError('Unexpected acceptance')
try:
 saved=(r/'results/status-forward-correspondence.json').read_bytes();bundle=json.loads(saved);d=m.inputs(r);cat=m.catalogue(d)
 returned=check('actual public semantic accepts pristine evidence',lambda:m.semantic(d,cat))
 returned[0]['declaration']['manager_fields']['declarations'].clear();returned[1]['instance_anchor']['instance']['binding']='bad';returned.clear()
 check('actual public saved receipt passes after nested semantic-result mutation',lambda:m.validate(r,saved))
 claims=[copy.deepcopy(c['internal_status_return_correspondence']) for c in bundle['contexts']];evidence=dict(m.inner(d)['ctx']['e']);path='evidence/execution-trace.json';trace=json.loads(evidence[path])
 for event in trace['events']:
  if event.get('function')=='ManagedAuthority.status' and event.get('event')=='return' and event.get('normal_return'):event['value']['connection_epoch']=17;event['state']['_epoch']=17
 evidence[path]=m.enc(trace)
 for row in claims:
  for sample in row['validated_manager_samples']:sample['value']['connection_epoch']=17;sample['snapshot']['_epoch']=17
 check('actual semantic rejects coordinated trace/snapshot/claim epoch substitution',lambda:reject(lambda:m.semantic(d,cat,claims,evidence)))
 badcat=copy.deepcopy(cat);badcat['ordered_hops'].pop();badcat['declarations'].pop()
 for row in claims:row['declaration']=copy.deepcopy(badcat);row['conditional_links'].pop()
 check('actual derivation rejects coordinated catalogue and both-context hop omission',lambda:reject(lambda:m.derive_status(d,badcat,claims)))
 bad=copy.deepcopy(bundle)
 for row in bad['contexts']:
  for sample in row['internal_status_return_correspondence']['validated_manager_samples']:sample['value']['actual_admission']=0
 check('actual public validation rejects wrong constant type',lambda:reject(lambda:m.validate(r,m.enc(bad))))
 print(json.dumps({'result':'PASS','checks':len(checks),'rows':checks,'seconds':time.monotonic()-start,'database_connections':0,'session_operations':0,'requests':0,'prior_suites_rerun':False},sort_keys=True),flush=True)
except BaseException as e:
 print(json.dumps({'result':'FAIL','checks':len(checks),'rows':checks,'error':repr(e),'traceback':traceback.format_exc(),'seconds':time.monotonic()-start},sort_keys=True),flush=True);raise
