from pathlib import Path
import copy,json,sys,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from oracle import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
class S(str):pass
class I(int):pass
class D(dict):pass
class L(list):pass
try:
 rec.save('input-verification.json',verify_root(root));guard(root);m=load(root/'code/correspondence.py');data=m.inputs(root);cat=m.catalogue(data)
 rec.save('source-oracle.json',rec.check('source independently fixes stages, ancestry, guards and unlink default',lambda:source_checks(m,data,cat)))
 print('Computing mandatory saved-evidence basis',flush=True)
 rows,b=m._checked(data,cat);c=data['coverage'];saved=(root/'results/primary/normal-session-exit-correspondence.json').read_bytes();bundle=m._assemble(data,rows,b)
 rec.check('mandatory token checker and underlying status derivation actually invoked',lambda:CALLS[(str(root/'retained/token/code/correspondence.py'),'_checked')]==1 and sum(v for (f,n),v in CALLS.items() if n=='derive_status')>=1)
 rec.check('receipt exactly reproduces saved bytes in ordered contexts',lambda:enc(bundle)==saved and [x['context'] for x in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
 rec.check('prior context fields preserved exactly',lambda:all(all(v==bundle['contexts'][i][k] for k,v in old.items()) for i,old in enumerate(b['prior']['contexts'])))
 cases=[]
 for idx in (0,1):
  tag=str(idx);fx=case(m,b,idx);cases.append(fx)
  def accept(label,q):
   return rec.check(tag+' '+label,lambda:m._construct_checked(b,q)['projection']==q['output'] and check_model(q))
  def reject(label,q):return rec.reject(tag+' '+label,lambda:m._construct_checked(b,q))
  accept('normal chain and independent milestone oracle',fx)
  for control,cont in [(False,True),(True,False)]:
   q=case(m,b,idx,control=control,continuity=cont);accept('source branches control='+str(control)+' continuity='+str(cont),q)
   rec.check(tag+' owner removal remains conditional '+str(cont),lambda q=q,cont=cont:q['output']['selected_owner_removed_in_model'] is (True if cont else None))
  for initial in [{'_live':None,'_retired':None,'_phase':'CLOSED'},{'_live':None,'_retired':'prior-retired','_phase':'CLEANUP_UNCERTAIN'},{'_live':'live-A','_retired':None,'_phase':'QUARANTINED'}]:
   q=case(m,b,idx,initial=initial);accept('normal close source-admitted '+initial['_phase'],q)
   rec.check(tag+' close reference subject '+initial['_phase'],lambda q=q,initial=initial:all(e['subject']['origin']=='initial:'+(initial['_live'] or initial['_retired']) for e in q['projection']['close_result']['events'] if e.get('kind')=='call:self._retired.close'))
  for marker in ('absent','UNKNOWN'):
   q=case(m,b,idx,terminal=('unlink-complete','missing-file'),marker=marker);accept('FileNotFoundError '+marker,q)
  accept('present namespace permits normal no-argument unlink',case(m,b,idx,marker='present'))
  for stage,kind in [('finally-enter','unobserved'),('removal-attempt','process-termination'),('removal-complete','unobserved')]:
   q=case(m,b,idx,token_terminal=(stage,kind));accept('no exit after token '+stage+' '+kind,q)
   bad=copy.deepcopy(q);bad['outcomes']=[{'stage':'session-resume','outcome':'normal'}];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('invented exit after incomplete token '+stage,bad)
  for stage in ORDER:
   for kind in ('unobserved','process-termination'):
    q=case(m,b,idx,terminal=(stage,kind));accept('prefix '+stage+' '+kind,q)
    bad=copy.deepcopy(q);bad['outcomes'].append({'stage':'unlink-complete','outcome':'normal'});bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('false continuation '+stage+' '+kind,bad)
  addr=next(e['address'] for e in fx['projection']['close_result']['events'] if e.get('kind')=='call:self._retired.close')
  failed=case(m,b,idx,terminal=('close-complete','raise'),close_outcomes={addr:'raise'});accept('underlying close raise blocks clear and unlink',failed)
  endaddr=next(e['address'] for e in fx['projection']['close_result']['events'] if e.get('kind')=='context-exit' and e['function']=='close')
  lockfail=case(m,b,idx,terminal=('close-complete','raise'),close_outcomes={endaddr:'raise'});accept('lock-exit failure after reference clear is still incomplete close',lockfail)
  rec.check(tag+' cleared reference and CLOSED phase insufficient for close completion',lambda:lockfail['projection']['close_result']['final']=={'_live':None,'_retired':None,'_phase':'CLOSED'} and not lockfail['output']['close_normal_completion_in_model'])
  partial=case(m,b,idx,terminal=('close-complete','process-termination'),close_outcomes={endaddr:'stop'});accept('partial close interpreter does not invent exception',partial)
  for q,label in [(failed,'raise'),(partial,'partial')]:
   bad=copy.deepcopy(q);bad['outcomes'][-1]['outcome']='normal';bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('false normal close '+label,bad)
  for stage in ('close-attempt','managed-clear','unlink-attempt','unlink-complete'):
   accept('modeled exception frontier '+stage,case(m,b,idx,terminal=(stage,'raise')))
  for path,val in [(('invocation',),'foreign-invocation'),(('context',),'SYMBOLIC-U-TWO' if idx==0 else 'SYMBOLIC-U-ONE'),(('anchor','instance','session_label'),'foreign-session'),(('anchor','instance','ownership_incarnation'),'0'*64),(('close_case','scope','acquisition'),'foreign-acquisition'),(('close_case','scope','instance'),'foreign-manager'),(('close_case','scope','invocation'),'other/managed-close'),(('close_case','method'),'state'),(('projection','references','owner','symbol'),'foreign-owner'),(('projection','references','manager','symbol'),'foreign-manager'),(('projection','references','session','symbol'),'foreign-wrapper'),(('projection','marker_path','component'),'active.json'),(('projection','marker_path','root'),'foreign-root'),(('projection','marker_path','nominal_recorded_path'),'/elsewhere/ACTIVE.json'),(('projection','marker_path','physical_resolved_path'),'/invented/ACTIVE.json'),(('projection','session_binding','recorded_destination'),'/elsewhere'),(('projection','session_binding','instance','binding'),'0'*64)]:reject('binding '+str(path),changed(fx,path,val))
  other=case(m,b,idx,inv='review-exit-002');accept('same-value distinct invocation',other)
  rec.check(tag+' occurrence identities distinguish repeated equal operations',lambda:set(e['id'] for e in fx['output']['events']).isdisjoint(e['id'] for e in other['output']['events']))
  bad=copy.deepcopy(fx);bad['token_case']=other['token_case'];reject('foreign pop predecessor',bad)
  bad=copy.deepcopy(fx);bad['projection']=other['projection'];bad['output']=other['output'];reject('coordinated foreign reports',bad)
  bad=copy.deepcopy(fx);bad['projection']['marker_path']['component']='WRONG.json';bad['output']['marker_path']=copy.deepcopy(bad['projection']['marker_path'])
  for e in bad['output']['events']:e['marker_path']=copy.deepcopy(bad['projection']['marker_path'])
  reject('coordinated marker reports still bound to source',bad)
  for i,stage in enumerate(ORDER):
   bad=copy.deepcopy(fx);del bad['outcomes'][i];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('omitted '+stage,bad)
  for i in (0,2,3,4,5):
   bad=copy.deepcopy(fx);bad['outcomes'][i:i+2]=reversed(bad['outcomes'][i:i+2]);bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('reordered adjacent '+str(i),bad)
  bad=copy.deepcopy(fx);bad['outcomes'].append(copy.deepcopy(bad['outcomes'][-1]));bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('duplicate completion',bad)
  bad=copy.deepcopy(fx);bad['close_case']=None;bad['projection']['close_result']=None;reject('normal completion requires close relation',bad)
  bad=copy.deepcopy(fx);bad['marker_at_unlink']='absent';bad['projection']['marker_at_unlink']='absent';reject('absent cannot produce successful unlink',bad)
  q=case(m,b,idx,terminal=('unlink-complete','missing-file'),marker='absent');q['marker_at_unlink']='present';q['projection']['marker_at_unlink']='present';reject('present contradicts missing-file',q)
  for path,typ in [(('invocation',),S),(('projection','session_binding'),D),(('close_case','initial','_phase'),S),(('projection','marker_path','session_binding','start_record','identity','bytes'),I),(('outcomes',),L),(('output','events'),L),(('output','completion'),S)]:
   p=fx
   for key in path:p=p[key]
   reject('exact type '+str(path),changed(fx,path,typ(p)))
  q=copy.deepcopy(fx);q['close_case']['initial']={S(k):v for k,v in q['close_case']['initial'].items()};reject('subclassed nested literal keys',q)
  for field,value in [('close_normal_completion_in_model',1),('marker_removal_completed_in_model',1),('physical_closure_established',True),('durability_established',True),('outer_context_exit_or_lock_release_established',True),('retained_error',{}),('actual_admission',True),('observer_join',{}),('runtime_exit_chain',[])]:reject('unsupported output '+field,changed(fx,('output',field),value))
  q=case(m,b,idx,terminal=('managed-clear','unobserved'));reject('premature clear',changed(q,('output','launcher_local_cleared_in_model'),True))
  q=case(m,b,idx,terminal=('unlink-complete','process-termination'));reject('termination cannot claim Python exception',changed(q,('output','terminal_python_exception_in_model'),True))
  out=m._construct_checked(b,fx);out['projection']['events'][0]['session_binding']['instance'].clear();out['projection']['reference_bindings']['manager']['scope']['instance'].clear();out['anchor'].clear();accept('nested returned aliases cannot change expectations',fx)
  for path,val in [(('conditional_links',),[]),(('session_binding','instance','session_label'),'foreign'),(('marker_path','component'),'elsewhere'),(('scope','invocation'),'invented'),(('runtime_exit_chain',),[]),(('classification',),'QUALIFIED')]:
   bad=copy.deepcopy(rows);target=bad[idx]
   for key in path[:-1]:target=target[key]
   target[path[-1]]=val;rec.reject(tag+' semantic claim '+str(path),lambda bad=bad:m._check_rows(b,bad))
  rec.check(tag+' producer validation consumes independently checked premises',lambda:c.validate_session_exit_projection(cat,fx['projection'],m._premises(b,fx),fx['output']))
 for field in ('guards','reference_edges','declarations'):
  bad=copy.deepcopy(cat);bad[field].pop();rec.reject('catalogue omitted '+field,lambda bad=bad:c.validate_session_exit(*m.sources(data),*m.dependencies(data),bad))
 for val in [[],list(reversed(rows)),[rows[0],rows[0]]]:rec.reject('semantic context domain '+str(len(val)),lambda val=val:m._check_rows(b,val))
 for label,e in [('missing',{k:v for k,v in b['evidence'].items() if k!='evidence/session-records/binding.json'}),('altered',dict(b['evidence']))]:
  if label=='altered':e['evidence/SMOKE-ABOUT-TO-START.json']=e['evidence/SMOKE-ABOUT-TO-START.json']+b' '
  rec.reject('actual evidence '+label,lambda e=e:m._compare_evidence(b,e))
 output=m._assemble(data,rows,b);output['contexts'].reverse();output['contexts'][0]['normal_session_exit_correspondence']['marker_path']['session_binding']['instance'].clear();output['extension_components'].clear()
 rec.check('returned bundle reversal and nested mutation isolate expectations',lambda:enc(m._assemble(data,rows,b))==saved)
 rec.check('all eleven obligations and UNKNOWNs preserved',lambda:bundle['unchanged_obligations']==b['prior']['unchanged_obligations'] and bundle['inventory_unknown_totals']==4 and bundle['lifetime_unknown_totals']==14 and bundle['new_normal_exit_limits']['actual_admission'] is False)
 rec.save('independent-fixtures.json',{'cases':cases});rec.save('receipt-identity.json',ident(saved));rec.save('final-root-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Fresh independent normal session-exit controls; no supplied suite rerun')
