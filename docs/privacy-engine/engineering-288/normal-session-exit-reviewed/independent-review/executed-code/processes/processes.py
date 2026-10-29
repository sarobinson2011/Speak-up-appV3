"""Fresh independent entry-point and distinct recovered-root checks."""
from pathlib import Path
import contextlib,copy,io,json,runpy,sys,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from oracle import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
try:
 rec.save('input-verification.json',verify_root(root));guard(root);m=load(root/'code/correspondence.py');saved=(root/'results/primary/normal-session-exit-correspondence.json').read_bytes();data=m.inputs(root);cat=m.catalogue(data)
 if mode=='recovered':
  rec.save('source-oracle.json',rec.check('recovered independent source/guard oracle',lambda:source_checks(m,data,cat)))
  rows,b=m._checked(data,cat);rec.check('recovered exact receipt',lambda:enc(m._assemble(data,rows,b))==saved)
  for idx in (0,1):
   tag=str(idx);fx=case(m,b,idx,inv='recovered-review-invocation',control=False,continuity=False)
   rec.check(tag+' recovered normal with explicit UNKNOWN continuity',lambda:m._construct_checked(b,fx)['projection']==fx['output'] and check_model(fx) and fx['output']['selected_owner_removed_in_model'] is None)
   q=case(m,b,idx,terminal=('unlink-complete','missing-file'),marker='absent');rec.check(tag+' recovered absent-file frontier keeps earlier facts',lambda:m._construct_checked(b,q)['projection']==q['output'] and check_model(q) and q['output']['launcher_local_cleared_in_model'] and q['output']['close_normal_completion_in_model'])
   for path,val in [(('output','marker_removal_completed_in_model'),True),(('output','authorization_renewed'),True),(('output','marker_namespace_fact'),'ABSENT-AT-UNLINK-COMPLETION')]:rec.reject(tag+' false missing-file summary '+str(path),lambda path=path,val=val:m._construct_checked(b,changed(q,path,val)))
   for path,val in [(('projection','references','manager','symbol'),'foreign'),(('projection','references','session','symbol'),'foreign'),(('close_case','scope','instance'),'foreign'),(('close_case','scope','invocation'),'old/managed-close'),(('projection','marker_path','nominal_recorded_path'),'/wrong/ACTIVE.json'),(('anchor','instance','session_label'),'wrong')]:rec.reject(tag+' recovered binding '+str(path),lambda path=path,val=val:m._construct_checked(b,changed(fx,path,val)))
   for stage in ('session-resume','close-complete','managed-clear','unlink-complete'):
    x=copy.deepcopy(fx);x['outcomes']=[v for v in x['outcomes'] if v['stage']!=stage];x['projection']['outcomes']=copy.deepcopy(x['outcomes']);rec.reject(tag+' recovered omitted '+stage,lambda x=x:m._construct_checked(b,x))
   x=case(m,b,idx,terminal=('close-complete','unobserved'));rec.check(tag+' recovered unobserved close is not closure',lambda:m._construct_checked(b,x)['projection']==x['output'] and check_model(x))
   for path,val in [(('output','close_normal_completion_in_model'),True),(('output','terminal_python_exception_in_model'),True),(('output','outer_cleanup_completion'),True)]:rec.reject(tag+' recovered unobserved escalation '+str(path),lambda path=path,val=val:m._construct_checked(b,changed(x,path,val)))
   got=m._construct_checked(b,fx);got['projection']['marker_path']['session_binding']['instance'].clear();got['projection']['events'].reverse();got['anchor'].clear();rec.check(tag+' recovered nested output isolated',lambda:m._construct_checked(b,fx)['projection']==fx['output'])
  out=m._assemble(data,rows,b);out['contexts'].reverse();out['contexts'][0]['normal_session_exit_correspondence']['declaration'].clear();rec.check('recovered returned context ordering isolated',lambda:enc(m._assemble(data,rows,b))==saved)
 elif mode=='semantic':
  rows=m.semantic(data,cat);pristine=copy.deepcopy(rows);rec.check('fresh semantic two exact contexts and unjoined observer',lambda:[r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and all(r['runtime_exit_chain'] is None and r['observer_join'] is None for r in rows))
  rows.reverse();rows[0]['marker_path']['session_binding']['instance'].clear();rows[1]['declaration']['source']['order'].clear()
  result=m.derive_exit(data,cat,pristine);rec.check('fresh derivation after nested returned mutations exactly pristine',lambda:enc(result)==saved)
  e=dict(m.inner(data)['ctx']['e']);k='evidence/SMOKE-ABOUT-TO-START.json';v=json.loads(e[k]);v['destination']='/invented-session';e[k]=enc(v);claims=copy.deepcopy(pristine)
  for row in claims:
   for sb in [row['session_binding'],row['marker_path']['session_binding']]:sb['recorded_destination']=v['destination'];sb['start_record']['identity']=ident(e[k])
   row['marker_path']['nominal_recorded_path']=v['destination']+'/ACTIVE.json'
  rec.reject('fresh semantic coordinated substituted saved destination and agreeing claims',lambda:m.semantic(data,cat,claims,e))
 elif mode=='constructed':
  fixture_path=Path(__file__).resolve().parents[1]/'primary/independent-fixtures.json';fx=json.loads(fixture_path.read_bytes())['cases']
  got=m.constructed_projection(data,cat,fx[1]);rec.check('fresh public constructed second-context relation',lambda:got['projection']==fx[1]['output'] and check_model(fx[1]))
  got['projection']['reference_bindings']['manager']['scope']['instance'].clear();got['projection']['events'].clear()
  bad=copy.deepcopy(fx[0]);bad['close_case']['scope']['instance']='foreign-manager';bad['projection']['close_result']['scope']['instance']='foreign-manager';bad['projection']['close_result']['case']['scope']['instance']='foreign-manager';bad['output']['managed_close_relation']=copy.deepcopy(bad['projection']['close_result'])
  rec.reject('fresh public constructed coordinated wrong-manager reports',lambda:m.constructed_projection(data,cat,bad))
 elif mode=='public':
  buf=io.StringIO();sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/normal-session-exit-correspondence.json')]
  with contextlib.redirect_stdout(buf):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  text=buf.getvalue();(rec.path/'CLI.stdout').write_text(text);answer=json.loads(text);rec.check('actual recovered CLI accepts exact both-context receipt',lambda:answer['result']=='PASS' and answer['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and answer['receipt']==ident(saved) and answer['actual_admission'] is False)
  for kind in ('missing-relation','duplicate-context','status-escalation'):
   val=json.loads(saved)
   if kind=='missing-relation':del val['contexts'][1]['normal_session_exit_correspondence']
   elif kind=='duplicate-context':val['contexts'][1]=copy.deepcopy(val['contexts'][0])
   else:val['new_normal_exit_limits']['actual_admission']=True
   rec.reject('public '+kind,lambda val=val:m.validate(root,enc(val)))
 else:raise ValueError(mode)
 rec.save('final-root-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Independent '+mode+' saved-input controls; no prior campaign repeated')
