import copy,json,sys,pathlib
import scope_integration as s
root=pathlib.Path(sys.argv[1]);out=pathlib.Path(sys.argv[2]);rows=[]
def ok(n,**d):
 rows.append({'case':n,'status':'PASS',**d});out.write_text(json.dumps(rows,indent=2))
def reject(n,fn):
 try:fn()
 except (ValueError,KeyError) as e:ok(n,rejection=str(e))
 else:raise AssertionError(n)
b=s.verified_inputs();s.preflight(root,b);ok('actual scope and complete current root preflight')
mutations=[('source-only changed',lambda x:x['scope']['assessment_target'].update(designation='OPERATIONAL')),('operator invented',lambda x:x['scope']['assessment_target'].update(operator_designated=True)),('unknown instances zero',lambda x:x['scope']['unknown_operational_sets'].update(managed_instances=0)),('finite lifetime',lambda x:x['scope'].update(global_lifetime_bound=384000)),('finite storage',lambda x:x['scope'].update(global_storage_byte_bound=0)),('missing carrier',lambda x:x['scope']['protected_logical_scope'].pop()),('omit obligation',lambda x:x['obligations']['obligations'].pop()),('coordinated exclusion',lambda x:(x['scope']['protected_logical_scope'].pop(),x['obligations']['obligations'].pop())),('discharge recovery',lambda x:x['obligations']['obligations'][4].update(current_status='CLOSED')),('stale candidate',lambda x:x['scope']['candidate_binding']['candidate'].update(sha256='0'*64)),('mixed contexts',lambda x:x['scope']['existing_context_associations']['associations'].reverse()),('missing family',lambda x:x['expressions']['families'].pop()),('missing directory',lambda x:x['expressions']['families'][0]['directory_ids'].pop()),('domain zero',lambda x:x['expressions']['families'][0].update(domain_value=0)),('wrong count equation',lambda x:x['expressions']['families'][0].update(expression=0)),('invented exclusion',lambda x:x['scope'].update(exclude_backups=True)),('stale obligation binding',lambda x:x['obligations']['scope_manifest_identity'].update(sha256='0'*64)),('admission true',lambda x:x['scope'].update(actual_admission=True)),('admission integer zero',lambda x:x['scope'].update(actual_admission=0))]
for n,f in mutations:
 x=copy.deepcopy(b);f(x);assert s.enc(x)!=s.enc(b);reject(n,lambda:s.preflight(root,x))
s.preflight(root,b);ok('pristine after mutations')
y=s.verified_inputs();y['scope']['protected_logical_scope'].clear();s.preflight(root,b);ok('returned input mutation does not poison expected inputs')
# No costly native replay is necessary for explicitly invalid result envelopes.
for n,r in [('legacy',{'format':'I164-CURRENT-BOUNDED-INTEGRATION-1'}),('false assurance',{'format':s.FORMAT,'operational_assurance':True}),('false zero',{'format':s.FORMAT,'operational_assurance':False,'global_lifetime_bound':0})]:reject(n,lambda:s.validate_result(root,r))
print('PASS',len(rows),'focused controls; no producer execution')
