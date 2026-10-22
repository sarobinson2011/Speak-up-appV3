import copy,json,pathlib,sys
import scope_integration as s
root=pathlib.Path(sys.argv[1]);saved=s.load(sys.argv[2]);out=pathlib.Path(sys.argv[3]);rows=[]
def reject(n,fn):
 try:fn()
 except ValueError as e:rows.append({'case':n,'status':'PASS','rejection':str(e)})
 else:raise AssertionError(n)
for n,fn in [('omitted result obligations',lambda x:x['obligations'].pop()),('reversed result contexts',lambda x:x['contexts'].reverse()),('result unknown changed to zero',lambda x:x['unknown_operational_sets'].update(session_databases=0)),('result assurance true',lambda x:x.update(operational_assurance=True)),('result finite global capacity',lambda x:x.update(global_storage_byte_bound=0)),('result readiness true',lambda x:x.update(full_expansion_ready=True)),('result admission integer false',lambda x:x.update(actual_admission=0)),('result missing final-binding',lambda x:x.pop('final_binding')),('result missing obligations',lambda x:x.pop('obligations'))]:
 bad=copy.deepcopy(saved);fn(bad);assert s.enc(bad)!=s.enc(saved);reject(n,lambda:s.validate_result(root,bad))
if len(sys.argv)>4:
 # The independent fresh execution/recovered-root result is the comparison, not
 # a hard-coded fixture expectation or a stored result accepted without validation.
 recovered=s.load(sys.argv[4]);s.same(saved,recovered,'RECOVERED-FRESH-RESULT');rows.append({'case':'independent processes roots identical complete result','status':'PASS'})
 assert saved['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and [r['context'] for r in saved['observations']]==saved['contexts'];assert all(r['response_associations']>0 for r in saved['observations']);rows.append({'case':'both contexts actual occurrence response and duty results','status':'PASS'})
out.write_text(json.dumps(rows,indent=2));print('PASS',len(rows),'serialized result and fresh-process correspondence checks')
