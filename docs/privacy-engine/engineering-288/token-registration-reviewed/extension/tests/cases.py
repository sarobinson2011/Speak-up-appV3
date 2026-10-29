import copy

def normal(m,basis,idx=0,control=True,continuity=True,invocation='constructed-run-A',owner_none=True,terminal=None):
 row=m._rows(basis)[idx];scope=m.invocation_scope(row['instance_anchor'],invocation);c=basis['fresh']['coverage'];cat=basis['catalogue']
 steps=['owner-create','token-create','registry-insert','control-guard']+(['control-create','control-callback'] if control else [])+['client-create','client-callback','owner-failure-guard','finally-enter','removal-attempt','removal-complete']
 outcomes=[]
 for stage in steps:
  out=terminal[1] if terminal and stage==terminal[0] else 'normal';outcomes.append({'stage':stage,'outcome':out})
  if out!='normal' or stage=='owner-failure-guard' and not owner_none:break
 validated={'occurrence':invocation,'scope':scope,'control_present':control,'owner_failure_none':owner_none,'registry_continuity':continuity,'outcomes':outcomes}
 projection={**copy.deepcopy(validated),'references':c.token_reference_premises(scope,control)};out=c.token_registration_projection(cat,projection,validated)
 return {'kind':'CONSTRUCTED-TOKEN-REGISTRATION','context':row['context'],'anchor':copy.deepcopy(row['instance_anchor']),'invocation':invocation,'control_present':control,'owner_failure_none':owner_none,'registry_continuity':continuity,'outcomes':copy.deepcopy(outcomes),'projection':projection,'output':out}

def premise(case):return {k:copy.deepcopy(v) for k,v in case['projection'].items() if k!='references'}
def change(v,path,value):
 v=copy.deepcopy(v);p=v
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return v
