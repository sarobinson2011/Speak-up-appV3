"""New bounded owner-finalization controls, using saved inputs/constructed cases only."""
from pathlib import Path
import sys,copy,json,ast,traceback,itertools
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);error=None
class S(str):pass
class I(int):pass
class D(dict):pass
class L(list):pass
try:
 mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);c=data['coverage'];bundle=m._assemble(data,rows,basis)
 rec.check('actual mandatory predecessor and status chain consumed',lambda:sum(x['function']=='_checked' and x['file'].endswith('retained/exit/code/correspondence.py') for x in CALLS)==1 and sum(x['function']=='derive_status' for x in CALLS)==1)
 rec.check('both symbolic contexts independently present',lambda:[r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
 rec.check('all prior context fields unchanged',lambda:all(all(bundle['contexts'][i][k]==v for k,v in row.items()) for i,row in enumerate(basis['prior']['contexts'])))
 # Independent source traversal supplies required origins/guards/order.
 t=ast.parse(m.sources(data)[0]);fn={n.name:n for n in t.body if isinstance(n,ast.FunctionDef)};lock=fn['owner_lock'];alloc=lock.body[-2];tr=lock.body[-1];close=tr.finalbody[0];outer=fn['_session'].body[-1]
 rec.check('fd producer precedes guarded yield',lambda:isinstance(alloc,ast.Assign) and ast.unparse(alloc.targets[0])=='fd' and ast.unparse(alloc.value.func)=='os.open' and ast.unparse(tr.body[-1])=='yield dest')
 rec.check('exact finalizer call and unchanged selected fd',lambda:len(tr.finalbody)==1 and ast.unparse(close)=='os.close(fd)' and not close.value.keywords and len(close.value.args)==1)
 writes=[n for n in ast.walk(lock) if isinstance(n,ast.Name) and n.id=='fd' and isinstance(n.ctx,ast.Store)];rec.check('single fd binding no source reassignment',lambda:len(writes)==1 and writes[0].lineno==112)
 rec.check('owner context contains normal unlink tail',lambda:ast.unparse(outer.items[0].context_expr)=='owner_lock(destination)' and ast.unparse(outer.body[-1].body[-1])=="(dest / 'ACTIVE.json').unlink()")
 expected=['owner-finalizer-enter','descriptor-close-attempt','descriptor-close-complete'];rec.check('independent expected stage coverage',lambda:cat['source']['order']==expected and [d['id'] for d in cat['declarations']]==expected)
 rec.check('descriptor source location independently matches',lambda:cat['source']['descriptor_slot']=='fd' and cat['source']['descriptor_assignment']['site'].split(':')[0]==str(alloc.lineno) and cat['source']['close_argument']['site'].split(':')[0]=='117')
 fixtures=[]
 for idx in (0,1):
  tag=rows[idx]['context'];fx=normal(m,basis,idx);fixtures.append(fx)
  def accept(label,q):return rec.check(label+' '+tag,lambda:m._construct_checked(basis,q)['projection']==q['output'])
  def reject(label,q):return rec.reject(label+' '+tag,lambda:m._construct_checked(basis,q))
  accept('normal selected descriptor finalization',fx)
  rec.check('three milestones established only in constructed normal path '+tag,lambda:fx['output']['finalizer_entry_completed_in_model'] and fx['output']['descriptor_close_attempt_entered_in_model'] and fx['output']['descriptor_close_normal_completion_in_model'] and not fx['output']['physical_lock_release_established'])
  no=normal(m,basis,idx,continuity=False);accept('unknown owner continuity preserved',no);rec.check('unknown continuity is not exclusive ownership '+tag,lambda:no['output']['selected_owner_removed_in_model'] is None and not no['output']['exclusive_ownership_established'])
  for stage in expected:
   for outcome in ('raise','process-termination','unobserved'):
    q=normal(m,basis,idx,terminal=(stage,outcome));accept(stage+' '+outcome,q)
    rec.check('no final close completion from '+stage+' '+outcome+' '+tag,lambda q=q,outcome=outcome:not q['output']['descriptor_close_normal_completion_in_model'] and q['output']['retained_error'] is None and not q['output']['authorization_renewed'] and (outcome=='raise' or q['output']['terminal_python_exception_in_model'] is None))
    bad=copy.deepcopy(q);bad['output']['descriptor_close_normal_completion_in_model']=True;reject('false completed-close '+stage+' '+outcome,bad)
    bad=copy.deepcopy(q);bad['outcomes'].append({'stage':'descriptor-close-complete','outcome':'normal'});bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('false continuation '+stage+' '+outcome,bad)
  for ex,marker in [(('unlink-complete','missing-file'),'absent'),(('unlink-complete','process-termination'),'UNKNOWN'),(('managed-clear','unobserved'),'UNKNOWN')]:
   q=normal(m,basis,idx,exit_terminal=ex,marker=marker);accept('outside normal route '+str(ex),q)
   rec.check('exceptional finalizer not modeled or disproved '+str(ex)+' '+tag,lambda q=q:q['output']['completion']=='outside-normal-finalization-slice' and q['output']['events']==[] and q['output']['exceptional_outer_cleanup_completion'] is None)
   bad=copy.deepcopy(q);bad['outcomes']=[{'stage':'owner-finalizer-enter','outcome':'normal'}];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('unsupported normal-route join '+str(ex),bad)
  for stage in expected:
   bad=copy.deepcopy(fx);bad['outcomes']=[r for r in bad['outcomes'] if r['stage']!=stage];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('omitted '+stage,bad)
  for perm in itertools.permutations(expected):
   if list(perm)==expected:continue
   bad=copy.deepcopy(fx);bad['outcomes']=[{'stage':s,'outcome':'normal'} for s in perm];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('reordered '+str(perm),bad)
  bad=copy.deepcopy(fx);bad['outcomes'].append(copy.deepcopy(bad['outcomes'][-1]));bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('duplicated completion',bad)
  for path,value in [(('projection','descriptor','slot'),'different_fd'),(('projection','descriptor','producer','site'),'1:0:1:1:Call'),(('projection','descriptor','source','sha256'),'0'*64),(('projection','descriptor','owner_lock_occurrence'),'foreign'),(('projection','descriptor','descriptor_result_occurrence'),'foreign'),(('projection','descriptor','scope','invocation'),'foreign'),(('projection','descriptor','lock_path','nominal_recorded_path'),'/foreign.owner.lock'),(('projection','descriptor','numeric_value'),9),(('projection','references','manager','symbol'),'foreign'),(('projection','session_binding','recorded_destination'),'/different'),(('anchor','instance','binding'),'stale')]:
   reject('substituted '+str(path),change(fx,path,value))
  other=normal(m,basis,idx,invocation='constructed-finalizer-B');rec.check('distinct call-result lineage despite no numeric evidence '+tag,lambda:fx['output']['descriptor_lineage']['descriptor_result_occurrence']!=other['output']['descriptor_lineage']['descriptor_result_occurrence'] and fx['output']['descriptor_lineage']['numeric_value'] is None and other['output']['descriptor_lineage']['numeric_value'] is None)
  bad=copy.deepcopy(fx);bad['projection']=copy.deepcopy(other['projection']);bad['output']=copy.deepcopy(other['output']);reject('coordinated foreign descriptor reports',bad)
  bad=copy.deepcopy(fx);bad['exit_case']=copy.deepcopy(other['exit_case']);reject('foreign predecessor invocation',bad)
  bad=copy.deepcopy(fx);bad['projection']['exit_result']['marker_removal_completed_in_model']=False;bad['output']['validated_normal_exit_prefix']=copy.deepcopy(bad['projection']['exit_result']);reject('coordinated stale predecessor report',bad)
  for field in ('physical_descriptor_closure_established','physical_lock_release_established','exclusive_ownership_established','durability_established','complete_outer_context_exit_established','authorization_renewed','actual_admission'):
   reject('unsupported '+field,change(fx,('output',field),True))
  for path,T in [(('invocation',),S),(('projection','descriptor'),D),(('outcomes',),L),(('output','completion'),S),(('output','events'),L),(('projection','descriptor','source','bytes'),I)]:
   q=copy.deepcopy(fx);v=q
   for k in path[:-1]:v=v[k]
   v[path[-1]]=T(v[path[-1]]);reject('exact type '+str(path),q)
  q=copy.deepcopy(fx);q['projection']['descriptor']={S(k):v for k,v in q['projection']['descriptor'].items()};reject('subclassed descriptor keys',q)
  reject('bool-int completion confusion',change(fx,('output','descriptor_close_normal_completion_in_model'),1))
  q=copy.deepcopy(fx);q['projection']['descriptor']=9;q['output']['descriptor_lineage']=9;reject('number alone cannot substitute lineage',q)
  got=m._construct_checked(basis,fx);got['projection']['descriptor_lineage']['scope']['instance'].clear();got['projection']['events'].clear();got['anchor'].clear();accept('nested returned mutations isolated',fx)
  for path,value in [(('conditional_links',),[]),(('descriptor_lineage','numeric_value'),9),(('descriptor_lineage','producer','site'),'wrong'),(('runtime_finalizer_chain',),[]),(('classification',),'KNOWN'),(('context',),rows[1-idx]['context'])]:
   q=copy.deepcopy(rows);v=q[idx]
   for k in path[:-1]:v=v[k]
   v[path[-1]]=value;rec.reject('semantic substituted '+str(path)+' '+tag,lambda q=q:m._check_rows(basis,q))
  q=copy.deepcopy(rows);q[idx]['descriptor_lineage']['source']['bytes']=I(q[idx]['descriptor_lineage']['source']['bytes']);rec.reject('semantic exact type before normalization '+tag,lambda:m._check_rows(basis,q))
  v=m._premises(basis,fx);rec.check('direct typed projection '+tag,lambda:c.validate_owner_finalization_projection(cat,fx['projection'],v,fx['output']))
  q=copy.deepcopy(fx['output']);q['descriptor_lineage']['scope'].clear();rec.reject('direct output substitution '+tag,lambda:c.validate_owner_finalization_projection(cat,fx['projection'],v,q))
  q=copy.deepcopy(fx['projection']);q['descriptor']['slot']=S(q['descriptor']['slot']);rec.reject('direct pre-serialization subclass gate '+tag,lambda:c.owner_finalization_projection(cat,q,v))
 for label,edit in [('missing declaration',lambda x:x['declarations'].pop()),('missing guard',lambda x:x['guard_branches'].pop('ordered_normal_prefix')),('wrong callee',lambda x:x['source'].update(close_callee='os.unlink')),('wrong argument',lambda x:x['source'].update(close_arguments=['other_fd'])),('wrong order',lambda x:x['source']['order'].reverse()),('wrong producer',lambda x:x['descriptor_declaration'].update(slot='other'))]:
  q=copy.deepcopy(cat);edit(q);rec.reject('source-derived oracle '+label,lambda q=q:c.validate_owner_finalization(m.sources(data)[0],m.dependency(data),q))
 e=dict(basis['evidence']);key='evidence/confirmed-close.json';d=json.loads(e[key]);d['cooperative_lock_reacquired']=False;e[key]=m.enc(d);rec.reject('candidate evidence must match consumed predecessor',lambda:m._compare_evidence(basis,e))
 before=m.enc(m._assemble(data,rows,basis));bundle['contexts'][0]['owner_lock_finalization_correspondence']['descriptor_lineage'].clear();bundle['contexts'].clear();rec.check('receipt output mutation cannot alter expectations',lambda:m.enc(m._assemble(data,rows,basis))==before)
 rec.check('unknowns and unjoined observer preserved',lambda:all(r['runtime_finalizer_chain'] is None and r['observer_join'] is None and r['classification']=='UNKNOWN' for r in rows))
 rec.save('fixtures.json',{'cases':fixtures});rec.save('owner-lock-finalization.json',m._assemble(data,rows,basis));rec.save('receipt-identity.json',identity(before))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='New Engineering owner-finalization controls only; prior independent and supplied results separate')
