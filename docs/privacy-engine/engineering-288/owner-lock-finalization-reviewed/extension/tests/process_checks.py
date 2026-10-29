"""Focused fresh-process and recovered-root controls; no previous suite is run."""
from pathlib import Path
import sys,copy,json,traceback,runpy,contextlib,io
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
try:
 rec.save('input-verification.json',verify_root(root));mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);saved=(root/'results/primary/owner-lock-finalization.json').read_bytes();data=m.inputs(root);cat=m.catalogue(data)
 if mode=='semantic':
  rows=m.semantic(data,cat);rec.check('fresh semantic both contexts',lambda:len(rows)==2 and all(r['numeric_descriptor_observation'] is None for r in rows));rows[0]['descriptor_lineage']['scope']['instance'].clear();rows.reverse()
  bad=copy.deepcopy(cat);bad['source']['close_arguments']=['other_fd'];claims=[x['owner_lock_finalization_correspondence'] for x in json.loads(saved)['contexts']]
  for row in claims:row['declaration']=copy.deepcopy(bad)
  rec.reject('fresh coordinated catalogue and semantic substitution',lambda:m.semantic(data,bad,claims))
 elif mode=='derive':
  result=m.derive_owner(data,cat);rec.check('fresh exact canonical derivation',lambda:m.enc(result)==saved);result['contexts'][0]['owner_lock_finalization_correspondence']['descriptor_lineage'].clear();result['contexts'].clear()
  e=dict(m.inner(data)['ctx']['e']);key='evidence/SMOKE-ABOUT-TO-START.json';v=json.loads(e[key]);v['destination']+='/foreign';e[key]=m.enc(v);claims=[x['owner_lock_finalization_correspondence'] for x in json.loads(saved)['contexts']]
  for row in claims:
   row['session_binding']['recorded_destination']=v['destination'];row['descriptor_lineage']['session_binding']['recorded_destination']=v['destination'];row['descriptor_lineage']['lock_path']['nominal_recorded_path']+='/foreign'
  rec.reject('fresh coordinated evidence destination and lineage reports',lambda:m.derive_owner(data,cat,claims,e))
 elif mode=='public':
  oldargs=sys.argv;sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/owner-lock-finalization.json')];out=io.StringIO()
  try:
   with contextlib.redirect_stdout(out):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  finally:sys.argv=oldargs
  rec.save('CLI-result.json',json.loads(out.getvalue()));(rec.path/'CLI.stdout').write_text(out.getvalue());rec.check('actual fresh offline CLI exact receipt',lambda:json.loads(out.getvalue())['result']=='PASS')
  bad=json.loads(saved);bad['contexts'][0]['owner_lock_finalization_correspondence']['descriptor_lineage']['numeric_value']=7;rec.reject('public altered descriptor claim',lambda:m.validate(root,m.enc(bad)))
  bad=json.loads(saved);del bad['contexts'][1]['owner_lock_finalization_correspondence'];rec.reject('public required second relation',lambda:m.validate(root,m.enc(bad)))
 elif mode=='constructed':
  fixtures=json.loads((root/'results/primary/fixtures.json').read_bytes())['cases'];got=m.constructed_projection(data,cat,fixtures[0]);rec.check('fresh public constructed acceptance',lambda:got['projection']==fixtures[0]['output']);got['projection']['events'].clear();got['anchor'].clear()
  bad=copy.deepcopy(fixtures[1]);bad['projection']['descriptor']['descriptor_result_occurrence']='foreign';bad['output']['descriptor_lineage']=copy.deepcopy(bad['projection']['descriptor']);rec.reject('fresh public coordinated descriptor substitution',lambda:m.constructed_projection(data,cat,bad))
 elif mode=='recovered':
  rows,basis=m._checked(data,cat);rec.check('recovered exact canonical receipt',lambda:m.enc(m._assemble(data,rows,basis))==saved)
  for idx in (0,1):
   fx=normal(m,basis,idx,continuity=False);rec.check('recovered normal with unknown continuity '+str(idx),lambda:m._construct_checked(basis,fx)['projection']==fx['output'] and fx['output']['selected_owner_removed_in_model'] is None)
   for stage in cat['source']['order']:
    for outcome in ('raise','process-termination','unobserved'):
     q=normal(m,basis,idx,terminal=(stage,outcome));rec.check('recovered frontier '+str(idx)+stage+outcome,lambda q=q:m._construct_checked(basis,q)['projection']==q['output']);q['output']['descriptor_close_normal_completion_in_model']=True;rec.reject('recovered false closure '+str(idx)+stage+outcome,lambda q=q:m._construct_checked(basis,q))
    q=copy.deepcopy(fx);q['outcomes']=[r for r in q['outcomes'] if r['stage']!=stage];q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject('recovered omitted step '+stage+str(idx),lambda q=q:m._construct_checked(basis,q))
   for path,value in [(('projection','descriptor','numeric_value'),11),(('projection','descriptor','scope','invocation'),'wrong'),(('projection','descriptor','lock_path','nominal_recorded_path'),'/wrong'),(('exit_case','invocation'),'foreign')]:
    q=change(fx,path,value);rec.reject('recovered binding '+str(idx)+str(path),lambda q=q:m._construct_checked(basis,q))
   got=m._construct_checked(basis,fx);got['projection']['descriptor_lineage'].clear();got['projection']['validated_normal_exit_prefix'].clear();rec.check('recovered nested output isolation '+str(idx),lambda:m._construct_checked(basis,fx)['projection']==fx['output'])
   q=copy.deepcopy(rows);q[idx]['conditional_links'].clear();rec.reject('recovered semantic missing relation '+str(idx),lambda:m._check_rows(basis,q))
 else:raise ValueError('UNKNOWN-MODE')
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,mode=mode,scope='New Engineering owner-finalization process controls only; prior reviews separate')
