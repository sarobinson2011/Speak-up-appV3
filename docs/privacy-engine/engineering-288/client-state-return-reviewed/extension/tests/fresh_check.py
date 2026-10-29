import copy,json,runpy,sys,time,types
from pathlib import Path
r=Path(sys.argv[1]).resolve();runpy.run_path(str(r/'tests/guard.py'))['install'](r)
p=r/'code/correspondence.py';m=types.ModuleType('_client_state_fresh');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__)
start=time.monotonic();rows=[]
def check(name,fn):
 result=fn();assert result is not False,name;rows.append({'check':name,'result':'PASS'});print('PASS '+name,flush=True);return result
def reject(fn):
 try:fn()
 except ValueError:return True
 raise AssertionError('Unexpected acceptance')
saved=(r/'results/client-state-correspondence.json').read_bytes();result=check('fresh public saved receipt',lambda:m.validate(r,saved))
d=m.inputs(r);cat=m.catalogue(d);c=d['coverage'];bundle=json.loads(saved)
fixtures=json.loads((r/'fixtures/normal-cases.json').read_bytes())
for record in fixtures['cases']:
 case=record['case'];original=copy.deepcopy(case['projection']);next_call=copy.deepcopy(original);invocation=original['occurrence']+':second-distinct';scope=m.invocation_scope(case['anchor'],invocation)
 def rescope(v):
  if type(v) is dict:
   for k,x in list(v.items()):
    if k=='scope':v[k]=copy.deepcopy(scope)
    else:rescope(x)
  elif type(v) is list:
   for x in v:rescope(x)
 rescope(next_call);next_call['occurrence']=invocation
 a=c.client_state_projection(cat,original,{'scope':original['scope'],'state':case['anchor']['validated_state']});b=c.client_state_projection(cat,next_call,{'scope':scope,'state':case['anchor']['validated_state']})
 check('equal values preserve distinct invocation/hop identities '+case['context'],lambda:a['hops'][-1]['value']==b['hops'][-1]['value'] and {h['id'] for h in a['hops']}.isdisjoint(h['id'] for h in b['hops']) and a['scope']!=b['scope'])
claims=[copy.deepcopy(x['client_state_return_correspondence']) for x in bundle['contexts']];evidence=dict(m.inner(d)['ctx']['e']);path='evidence/recovery-export-0.json';export=json.loads(evidence[path]);head=json.loads(bytes.fromhex(export['head']));head['head']='f'*64;export['head']=m.enc(head).hex();evidence[path]=m.enc(export)
for claim in claims:
 claim['validated_state_anchor']['validated_state']['head']='f'*64
 for link in claim['conditional_links']:link['conditional_value_at_validated_frontier']['head']='f'*64
check('actual semantic rejects coordinated evidence and both-context claims',lambda:reject(lambda:m.semantic(d,cat,claims,evidence)))
badcat=copy.deepcopy(cat);badcat['copy_semantics']['algorithm']='deepcopy preserves aliases'
for claim in claims:claim['declaration']=copy.deepcopy(badcat)
check('actual derivation rejects coordinated source-catalogue and claims',lambda:reject(lambda:m.derive_client_state(d,badcat,claims)))
print(json.dumps({'result':'PASS','checks':len(rows),'rows':rows,'seconds':time.monotonic()-start,'public_result':result,'constructed_not_runtime':True,'database_connections':0,'session_operations':0,'requests':0},sort_keys=True),flush=True)
