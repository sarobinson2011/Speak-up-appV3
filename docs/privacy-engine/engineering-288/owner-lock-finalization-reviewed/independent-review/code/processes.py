"""Independent fresh-process and recovered-root controls over saved inputs only."""
from pathlib import Path
import contextlib,copy,io,json,runpy,sys,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from oracle import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);mode=sys.argv[3];error=None
try:
 rec.save('input-verification.json',verify_root(root));guard(root);m=load(root/'code/correspondence.py');data=m.inputs(root);cat=m.catalogue(data);saved=(root/'results/primary/owner-lock-finalization.json').read_bytes()
 if mode=='recovered':
  rec.save('source-oracle.json',rec.check('fresh recovered source/guard oracle',lambda:source_check(m,data,cat)))
  rows,b=m._checked(data,cat);rec.check('recovered exact two-context receipt',lambda:enc(m._assemble(data,rows,b))==saved)
  for idx in (0,1):
   tag=str(idx);fx=case(m,b,idx,inv='recovered-finalizer',continuity=False,control=False)
   rec.check(tag+' normal source path with unknown owner continuity',lambda:m._construct_checked(b,fx)['projection']==fx['output'] and check_model(fx) and fx['output']['selected_owner_removed_in_model'] is None)
   for stage,kind in [(ORDER[0],'unobserved'),(ORDER[1],'process-termination'),(ORDER[2],'raise')]:
    q=case(m,b,idx,terminal=(stage,kind));rec.check(tag+' recovered frontier '+stage+' '+kind,lambda q=q:m._construct_checked(b,q)['projection']==q['output'] and check_model(q));rec.reject(tag+' false normal completion '+stage,lambda q=q:m._construct_checked(b,change(q,('output','descriptor_close_normal_completion_in_model'),True)))
   q=case(m,b,idx,exit_terminal=('unlink-complete','missing-file'),marker='absent');rec.check(tag+' exceptional predecessor remains unexpanded not disproved',lambda:m._construct_checked(b,q)['projection']==q['output'] and check_model(q));q['outcomes']=[{'stage':ORDER[0],'outcome':'normal'}];q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject(tag+' false normal-route join',lambda:m._construct_checked(b,q))
   for i,stage in enumerate(ORDER):
    q=copy.deepcopy(fx);del q['outcomes'][i];q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject(tag+' omitted '+stage,lambda q=q:m._construct_checked(b,q))
    q=copy.deepcopy(fx);q['outcomes'].insert(i,copy.deepcopy(q['outcomes'][i]));q['projection']['outcomes']=copy.deepcopy(q['outcomes']);rec.reject(tag+' duplicate '+stage,lambda q=q:m._construct_checked(b,q))
   for path,val in [(('projection','descriptor','numeric_value'),9),(('projection','descriptor','scope','invocation'),'foreign'),(('projection','descriptor','lock_path','nominal_recorded_path'),'/wrong'),(('exit_case','invocation'),'foreign'),(('output','physical_lock_release_established'),True),(('output','descriptor_close_attempt_entered_in_model'),1)]:rec.reject(tag+' recovered substitution '+str(path),lambda path=path,val=val:m._construct_checked(b,change(fx,path,val)))
   got=m._construct_checked(b,fx);got['projection']['descriptor_lineage']['scope']['instance'].clear();got['projection']['events'].reverse();rec.check(tag+' nested result isolation',lambda:m._construct_checked(b,fx)['projection']==fx['output'])
   claims=copy.deepcopy(rows);claims[idx]['conditional_links'].clear();rec.reject(tag+' missing semantic relation',lambda:m._check_rows(b,claims))
  out=m._assemble(data,rows,b);out['contexts'].reverse();out['contexts'][0]['owner_lock_finalization_correspondence']['descriptor_lineage'].clear();rec.check('recovered bundle expectation isolation',lambda:enc(m._assemble(data,rows,b))==saved)
 elif mode=='semantic':
  rows=m.semantic(data,cat);pristine=copy.deepcopy(rows);rec.check('fresh semantic both contexts with unobserved descriptor',lambda:[x['context'] for x in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and all(x['numeric_descriptor_observation'] is None and x['observer_join'] is None for x in rows))
  rows.reverse();rows[0]['descriptor_lineage']['scope']['instance'].clear();rows[1]['declaration']['source']['close_arguments'].append('foreign')
  derived=m.derive_owner(data,cat,pristine);rec.check('fresh derivation remains pristine after nested result mutation',lambda:enc(derived)==saved)
  e=dict(m.inner(data)['ctx']['e']);key='evidence/SMOKE-ABOUT-TO-START.json';x=json.loads(e[key]);x['destination']='/foreign-session';e[key]=enc(x);claims=copy.deepcopy(pristine)
  for row in claims:
   row['session_binding']['recorded_destination']=x['destination'];row['session_binding']['start_record']['identity']=ident(e[key]);row['descriptor_lineage']['session_binding']=copy.deepcopy(row['session_binding']);row['descriptor_lineage']['lock_path']['nominal_recorded_path']='/.foreign-session.owner.lock'
  rec.reject('fresh semantic coordinated saved-destination and lineage substitution',lambda:m.semantic(data,cat,claims,e))
 elif mode=='constructed':
  fx=json.loads((Path(__file__).resolve().parents[1]/'primary/independent-fixtures.json').read_bytes())['cases'];got=m.constructed_projection(data,cat,fx[1]);rec.check('fresh public constructed second-context acceptance',lambda:got['projection']==fx[1]['output'] and check_model(fx[1]));got['projection']['descriptor_lineage']['producer'].clear();got['projection']['events'].clear()
  bad=copy.deepcopy(fx[0]);bad['projection']['descriptor']['descriptor_result_occurrence']='foreign/owner-lock/os.open-result';bad['output']['descriptor_lineage']=copy.deepcopy(bad['projection']['descriptor'])
  for e in bad['output']['events']:e['descriptor_result_occurrence']=bad['projection']['descriptor']['descriptor_result_occurrence'];e['descriptor']=copy.deepcopy(bad['projection']['descriptor'])
  rec.reject('fresh public coordinated wrong descriptor occurrence',lambda:m.constructed_projection(data,cat,bad))
 elif mode=='public':
  stream=io.StringIO();sys.argv=[str(root/'code/correspondence.py'),'--root',str(root),'--receipt',str(root/'results/primary/owner-lock-finalization.json')]
  with contextlib.redirect_stdout(stream):runpy.run_path(str(root/'code/correspondence.py'),run_name='__main__')
  text=stream.getvalue();(rec.path/'CLI.stdout').write_text(text);answer=json.loads(text);rec.check('actual fresh recovered CLI binds both contexts and exact receipt',lambda:answer['result']=='PASS' and answer['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and answer['receipt']==ident(saved) and answer['runtime_finalizer_chain']=='UNAVAILABLE' and answer['actual_admission'] is False)
  bad=json.loads(saved);bad['contexts'][0]['owner_lock_finalization_correspondence']['descriptor_lineage']['numeric_value']=9;rec.reject('public invented descriptor observation',lambda:m.validate(root,enc(bad)))
  bad=json.loads(saved);del bad['contexts'][1]['owner_lock_finalization_correspondence'];rec.reject('public second relation mandatory',lambda:m.validate(root,enc(bad)))
  legacy=(root/'retained/exit/results/primary/normal-session-exit-correspondence.json').read_bytes();rec.reject('reviewed predecessor cannot replace current mandatory entry',lambda:m.validate(root,legacy))
 else:raise ValueError('UNKNOWN-MODE')
 rec.save('final-root-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Fresh independent '+mode+' owner-finalization controls; no completed suite repeated')
