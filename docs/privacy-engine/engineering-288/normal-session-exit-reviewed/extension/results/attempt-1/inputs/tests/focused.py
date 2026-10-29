"""Focused new normal-exit controls. Earlier suites are retained, never rerun."""
from pathlib import Path
import sys,copy,json,traceback,ast
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);error=None;write='--write' in sys.argv
class S(str):pass
class D(dict):pass
class L(list):pass
class I(int):pass
try:
 if not write:rec.save('input-verification.json',verify_root(root))
 mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);c=data['coverage'];bundle=m._assemble(data,rows,basis)
 rec.check('mandatory token checker and underlying status chain invoked',lambda:sum(x['function']=='derive_status' for x in CALLS)==1 and sum(x['function']=='_checked' and x['file'].endswith('retained/token/code/correspondence.py') for x in CALLS)==1)
 rec.check('both required contexts exact',lambda:[r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
 rec.check('prior fields exact and untouched',lambda:all(all(v==bundle['contexts'][i][k] for k,v in ctx.items()) for i,ctx in enumerate(basis['prior']['contexts'])))
 launcher,entry,manager=m.sources(data);tree=ast.parse(launcher);f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session');tr=f.body[-1].body[-1]
 rec.check('independent source normal tail order',lambda:[ast.unparse(n) for n in tr.body[-4:]]==['yield ManagedSession(managed)','managed.close()','managed = None',"(dest / 'ACTIVE.json').unlink()"])
 unlink=tr.body[-1].value;rec.check('unlink no existence guard and no missing_ok override',lambda:not unlink.args and not unlink.keywords and isinstance(tr.body[-1],ast.Expr) and ast.unparse(tr.handlers[0].type)=='BaseException')
 order=['session-resume','launcher-resume','close-attempt','close-complete','managed-clear','unlink-attempt','unlink-complete'];rec.check('independent expected stage coverage',lambda:cat['source']['order']==order and [d['id'] for d in cat['declarations']]==order)
 fixtures=[]
 for idx in (0,1):
  tag=rows[idx]['context'];fx=normal(m,basis,idx);fixtures.append(fx)
  def accepted(label,case):return rec.check(label+' '+tag,lambda:m._construct_checked(basis,case)['projection']==case['output'])
  def reject(label,case):return rec.reject(label+' '+tag,lambda:m._construct_checked(basis,case))
  accepted('normal pop close clear unlink',fx)
  for phase in ('CLOSED','QUARANTINED','CLEANUP_UNCERTAIN','OPEN_FAILED','VALIDATION_FAILED'):
   accepted('source admitted close without READY '+phase,normal(m,basis,idx,phase=phase,live=None))
  no=normal(m,basis,idx,continuity=False);accepted('unknown continuity still permits normal launcher continuation',no)
  rec.check('continuity not upgraded to selected owner removal',lambda:no['output']['selected_owner_removed_in_model'] is None and not no['output']['runtime_exclusivity_established'])
  missing=normal(m,basis,idx,terminal=('unlink-complete','missing-file'),marker='absent');accepted('absent unlink raises after close and clear',missing)
  rec.check('missing marker not unlink completion or durability',lambda:missing['output']['close_normal_completion_in_model'] and missing['output']['launcher_local_cleared_in_model'] and not missing['output']['marker_removal_completed_in_model'] and missing['output']['exception_class']=='FileNotFoundError' and not missing['output']['durability_established'])
  stopped=normal(m,basis,idx,token_terminal=('removal-complete','unobserved'));accepted('non-normal predecessor cannot enter session exit',stopped)
  rec.check('saved marker absence cannot synthesize exit steps',lambda:stopped['output']['events']==[] and not stopped['output']['close_normal_completion_in_model'])
  for stage in order:
   for outcome in ('process-termination','unobserved'):
    q=normal(m,basis,idx,terminal=(stage,outcome));accepted(stage+' '+outcome,q)
    rec.check('no Python unwind cleanup inference '+stage+' '+outcome+' '+tag,lambda q=q:q['output']['terminal_python_exception_in_model'] is None and q['output']['retained_error'] is None and q['output']['outer_cleanup_completion'] is None and not q['output']['authorization_renewed'])
    bad=copy.deepcopy(q);bad['outcomes'].append({'stage':'unlink-complete','outcome':'normal'});bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('false continuation '+stage+' '+outcome,bad)
  # Actual old close interpreter supplies an abrupt path; no invented close receipt.
  addr=next(e['address'] for e in fx['projection']['close_result']['events'] if e.get('kind')=='call:self._retired.close')
  abrupt=normal(m,basis,idx,terminal=('close-complete','raise'),close_outcomes={addr:'raise'});accepted('managed close failure frontier',abrupt)
  rec.check('failed managed close forbids local clear and marker removal',lambda:not abrupt['output']['launcher_local_cleared_in_model'] and not abrupt['output']['marker_removal_completed_in_model'])
  for stage in ('session-resume','launcher-resume','close-attempt','managed-clear','unlink-attempt','unlink-complete'):
   accepted('explicit exception frontier '+stage,normal(m,basis,idx,terminal=(stage,'raise')))
  for path in [('projection','references','manager','symbol'),('projection','references','session','symbol'),('projection','marker_path','component'),('projection','marker_path','root'),('projection','marker_path','nominal_recorded_path'),('projection','session_binding','recorded_destination'),('close_case','scope','instance'),('close_case','scope','invocation'),('anchor','instance','binding')]:
   reject('wrong binding '+str(path),change(fx,path,'foreign'))
  other=normal(m,basis,idx,invocation='constructed-exit-B');bad=copy.deepcopy(fx);bad['projection']=copy.deepcopy(other['projection']);bad['output']=copy.deepcopy(other['output']);reject('coordinated foreign invocation',bad)
  rec.check('distinct invocation retains distinct exit occurrences '+tag,lambda:fx['output']['events'][0]['id']!=other['output']['events'][0]['id'])
  bad=copy.deepcopy(fx);bad['token_case']=copy.deepcopy(other['token_case']);reject('foreign normal-pop predecessor',bad)
  bad=copy.deepcopy(fx);bad['close_case']['method']='recover';reject('wrong method close predecessor',bad)
  bad=copy.deepcopy(fx);bad['projection']['close_result']['final']['_phase']='READY';bad['output']['managed_close_relation']=copy.deepcopy(bad['projection']['close_result']);reject('coordinated close report substitution',bad)
  for stage in order:
   bad=copy.deepcopy(fx);bad['outcomes']=[r for r in bad['outcomes'] if r['stage']!=stage];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('omitted '+stage,bad)
  bad=copy.deepcopy(fx);bad['outcomes'][4],bad['outcomes'][5]=bad['outcomes'][5],bad['outcomes'][4];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('unlink before local clear',bad)
  bad=copy.deepcopy(fx);bad['marker_at_unlink']='absent';bad['projection']['marker_at_unlink']='absent';reject('absent no-argument unlink cannot return normal',bad)
  bad=copy.deepcopy(missing);bad['marker_at_unlink']='present';bad['projection']['marker_at_unlink']='present';reject('present contradicts missing-file outcome',bad)
  bad=copy.deepcopy(fx);bad['close_case']=None;bad['projection']['close_result']=None;reject('normal close without validated close correspondence',bad)
  for field,value in [('physical_closure_established',True),('runtime_exclusivity_established',True),('durability_established',True),('observer_join',{}),('outer_cleanup_completion',True),('selected_owner_removed_in_model',True)]:
   bad=copy.deepcopy(no);bad['output'][field]=value;reject('unsupported output '+field,bad)
  for path,T in [(('invocation',),S),(('projection','references'),D),(('outcomes',),L),(('output','completion'),S),(('output','events'),L),(('projection','session_binding','start_record','identity','bytes'),I)]:
   bad=copy.deepcopy(fx);p=bad
   for k in path[:-1]:p=p[k]
   p[path[-1]]=T(p[path[-1]]);reject('exact type '+str(path),bad)
  bad=copy.deepcopy(fx);bad['output']['events'][0]={S(k):v for k,v in bad['output']['events'][0].items()};reject('nested subclassed literal keys',bad)
  bad=copy.deepcopy(fx);bad['output']['marker_removal_completed_in_model']=1;reject('boolean integer substitution',bad)
  out=m._construct_checked(basis,fx);out['projection']['reference_bindings']['manager']['scope']['instance'].clear();out['projection']['events'].clear();out['anchor'].clear();accepted('nested returned mutations cannot change expectations',fx)
  for path,value in [(('conditional_links',),[]),(('marker_path','component'),'elsewhere'),(('saved_close_evidence','value','active_marker_absent'),False),(('scope','invocation'),'invented'),(('runtime_exit_chain',),[]),(('context',),rows[1-idx]['context'])]:
   bad=copy.deepcopy(rows);p=bad[idx]
   for k in path[:-1]:p=p[k]
   p[path[-1]]=value;rec.reject('semantic altered '+str(path)+' '+tag,lambda bad=bad:m._check_rows(basis,bad))
  v=m._premises(basis,fx);rec.check('direct producer output acceptance '+tag,lambda:c.validate_session_exit_projection(cat,fx['projection'],v,fx['output']))
  bad=copy.deepcopy(fx['output']);bad['events']=L(bad['events']);rec.reject('direct producer exact output gate '+tag,lambda:c.validate_session_exit_projection(cat,fx['projection'],v,bad))
 for label,edit in [('omitted declaration',lambda x:x['declarations'].pop()),('omitted guard',lambda x:x['guards'].pop()),('reordered',lambda x:x['source']['order'].reverse()),('missing-file suppression',lambda x:x['source'].update(missing_ok_argument=True)),('stale source',lambda x:x['source']['launcher'].update(sha256='0'*64))]:
  bad=copy.deepcopy(cat);edit(bad);rec.reject('source '+label,lambda bad=bad:c.validate_session_exit(*m.sources(data),*m.dependencies(data),bad))
 e=dict(basis['evidence']);e['evidence/confirmed-close.json']=e['evidence/confirmed-close.json'].replace(b'"active_marker_absent": true',b'"active_marker_absent": false');require_change=e!=basis['evidence'];rec.check('evidence mutation changed actual bytes',lambda:require_change);rec.reject('altered saved evidence despite agreeing report',lambda:m._compare_evidence(basis,e))
 before=m.enc(m._assemble(data,rows,basis));bundle['contexts'][0]['normal_session_exit_correspondence']['declaration'].clear();bundle['contexts'].clear();rec.check('bundle output aliases isolated',lambda:m.enc(m._assemble(data,rows,basis))==before)
 rec.check('saved close observer unjoined and unknown counts retained',lambda:all(r['saved_close_evidence']['join_to_selected_constructed_invocation'] is None and r['observer_join'] is None and r['classification']=='UNKNOWN' for r in rows))
 receipt=m.enc(m._assemble(data,rows,basis));rec.save('fixtures.json',{'cases':fixtures});rec.save('receipt-identity.json',identity(receipt))
 if write:rec.save('normal-session-exit-correspondence.json',json.loads(receipt))
 else:rec.check('recovered exact receipt reproduction',lambda:(root/'results/primary/normal-session-exit-correspondence.json').read_bytes()==receipt)
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='New Engineering supplied normal-session-exit controls; previous results remain separate')
