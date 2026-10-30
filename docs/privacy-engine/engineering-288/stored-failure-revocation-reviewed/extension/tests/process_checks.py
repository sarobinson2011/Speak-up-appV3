"""Focused new fresh/recovered checks, never a previous campaign."""
from pathlib import Path
import sys,copy,json,traceback,runpy,contextlib,io
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
try:
 rec.save('input-verification.json',verify_root(root));mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);saved=(root/'results/primary/stored-failure-revocation.json').read_bytes();data=m.inputs(root);cat=m.catalogue(data)
 if mode=='fresh':
  rows=m.semantic(data,cat);rec.check('fresh semantic both contexts and absent runtime observations',lambda:len(rows)==2 and all(r['runtime_stored_failure_chain'] is None for r in rows));rows[0]['failure_predecessors'].clear();rows.clear()
  e=dict(m.inner(data)['ctx']['e']);key='evidence/SMOKE-ABOUT-TO-START.json';v=json.loads(e[key]);v['destination']+='/foreign';e[key]=m.enc(v);claims=[r['stored_failure_revocation_correspondence'] for r in json.loads(saved)['contexts']]
  for r in claims:r['instance_anchor']['instance']['workspace']=v['destination'];r['scope']['instance']['workspace']=v['destination']
  rec.reject('fresh derive coordinated mixed evidence and reports',lambda:m.derive_stored(data,cat,claims,e))
 elif mode=='public':
  oldargs=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/stored-failure-revocation.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=oldargs
  rec.save('CLI-result.json',json.loads(out.getvalue()));(rec.path/'CLI.stdout').write_text(out.getvalue());rec.check('actual offline CLI canonical receipt',lambda:json.loads(out.getvalue())['result']=='PASS')
  q=json.loads(saved);q['contexts'][0]['stored_failure_revocation_correspondence']['guard_slot_premise']='established history';rec.reject('public altered continuity receipt',lambda:m.validate(root,m.enc(q)))
  q=json.loads(saved);del q['contexts'][1]['stored_failure_revocation_correspondence'];rec.reject('public second mandatory relation absent',lambda:m.validate(root,m.enc(q)))
 elif mode=='constructed':
  fixtures=json.loads((root/'results/primary/fixtures.json').read_bytes())['cases'];fx=fixtures[0];got=m.constructed_projection(data,cat,fx);rec.check('fresh public constructed handle accepted',lambda:got['projection']==fx['output']);got['projection']['original_error'].clear();got['anchor'].clear()
  q=copy.deepcopy(fixtures[3]);q['failure_result']['original_exception']['reference']='wrong/error';q['projection']['failure_provenance']=copy.deepcopy(q['failure_result']);q['projection']['stored_error_binding']['error']=copy.deepcopy(q['failure_result']['original_exception']);q['output']['original_error']=copy.deepcopy(q['failure_result']['original_exception']);rec.reject('fresh public coordinated state error substitution',lambda:m.constructed_projection(data,cat,q))
 elif mode=='recovered':
  rows,basis=m._checked(data,cat);rec.check('recovered exact canonical receipt',lambda:m.enc(m._assemble(data,rows,basis))==saved)
  for idx in (0,1):
   for route in ('handle','state'):
    q=normal(m,basis,idx,route=route,continuity=False);rec.check('recovered '+str(idx)+route+' unknown continuity',lambda q=q:m._construct_checked(basis,q)['projection']==q['output'] and q['output']['selected_owner_removed_in_model'] is None)
   fx=normal(m,basis,idx)
   for stage in cat['source']['order']:
    for outcome in ('raise','process-termination','unobserved'):
     q=normal(m,basis,idx,terminal=(stage,outcome));rec.check('recovered frontier '+str(idx)+stage+outcome,lambda q=q:m._construct_checked(basis,q)['projection']==q['output']);q['output']['run_success_established']=True;rec.reject('recovered false success '+str(idx)+stage+outcome,lambda q=q:m._construct_checked(basis,q))
    q=copy.deepcopy(fx);q['outcomes']=[x for x in q['outcomes'] if x['stage']!=stage];q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('recovered missing '+stage+str(idx),lambda q=q:m._construct_checked(basis,q))
   for path,value in [(('failure_result','original_exception','reference'),'wrong'),(('failure_input','references','token','symbol'),'wrong'),(('token_case','invocation'),'foreign'),(('projection','scope','instance','binding'),'0'*64), (('output','failure_storage_previously_completed_in_model'),False)]:
    q=change(fx,path,value);rec.reject('recovered binding '+str(idx)+str(path),lambda q=q:m._construct_checked(basis,q))
   got=m._construct_checked(basis,fx);got['projection']['stored_error_binding'].clear();got['projection']['validated_failure_provenance'].clear();rec.check('recovered result isolation '+str(idx),lambda:m._construct_checked(basis,fx)['projection']==fx['output'])
   claims=copy.deepcopy(rows);claims[idx]['conditional_links'].clear();rec.reject('recovered semantic omitted relation '+str(idx),lambda:m._check_rows(basis,claims))
 else:raise ValueError('UNKNOWN-MODE')
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='New Engineering stored-failure process controls; previous supplied and independent results separate')
