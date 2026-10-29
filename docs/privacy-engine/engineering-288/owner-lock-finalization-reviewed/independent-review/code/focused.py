from pathlib import Path
import copy,itertools,json,sys,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from oracle import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
class S(str):pass
class I(int):pass
class D(dict):pass
class L(list):pass
try:
 rec.save('input-verification.json',verify_root(root));guard(root);m=load(root/'code/correspondence.py');data=m.inputs(root);cat=m.catalogue(data);c=data['coverage']
 rec.save('source-oracle.json',rec.check('independent source assignment, guards, finalbody and ordered coverage',lambda:source_check(m,data,cat)))
 print('Validating actual predecessor chain over saved evidence',flush=True);rows,b=m._checked(data,cat);bundle=m._assemble(data,rows,b);saved=(root/'results/primary/owner-lock-finalization.json').read_bytes()
 rec.check('mandatory predecessor checker and underlying status chain actually execute',lambda:CALLS[(str(root/'retained/exit/code/correspondence.py'),'_checked')]==1 and sum(v for (f,n),v in CALLS.items() if n=='derive_status')>=1)
 rec.check('both contexts and exact canonical receipt',lambda:[r['context'] for r in rows]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and enc(bundle)==saved)
 rec.check('every predecessor context field preserved',lambda:all(all(bundle['contexts'][i][k]==v for k,v in old.items()) for i,old in enumerate(b['prior']['contexts'])))
 fixtures=[]
 for idx in (0,1):
  tag=str(idx);fx=case(m,b,idx);fixtures.append(fx)
  def accept(label,q):return rec.check(tag+' '+label,lambda:m._construct_checked(b,q)['projection']==q['output'] and check_model(q))
  def reject(label,q):return rec.reject(tag+' '+label,lambda:m._construct_checked(b,q))
  accept('normal path independently checked against ordered milestone oracle',fx)
  for control,continuity in [(False,True),(True,False)]:
   q=case(m,b,idx,control=control,continuity=continuity);accept('optional control='+str(control)+' conditional continuity='+str(continuity),q)
  for stage in ORDER:
   for kind in ('raise','process-termination','unobserved'):
    q=case(m,b,idx,terminal=(stage,kind));accept('stopped prefix '+stage+' '+kind,q)
    reject('false normal close '+stage+' '+kind,change(q,('output','descriptor_close_normal_completion_in_model'),True))
    bad=copy.deepcopy(q);bad['outcomes'].append({'stage':'descriptor-close-complete','outcome':'normal'});bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('invented continuation '+stage+' '+kind,bad)
    if kind!='raise':reject('termination or absence not Python exception '+stage+' '+kind,change(q,('output','terminal_python_exception_in_model'),True))
  # Non-normal predecessors remain outside this slice without erasing prior facts.
  for term,marker in [(('unlink-complete','missing-file'),'absent'),(('unlink-complete','raise'),'UNKNOWN'),(('unlink-complete','process-termination'),'UNKNOWN'),(('managed-clear','unobserved'),'UNKNOWN')]:
   q=case(m,b,idx,exit_terminal=term,marker=marker);accept('exceptional or incomplete predecessor '+str(term),q)
   rec.check(tag+' earlier close facts retained '+str(term),lambda q=q:q['output']['validated_normal_exit_prefix']==q['exit_case']['output'] and q['output']['events']==[] and q['output']['exceptional_outer_cleanup_completion'] is None)
   bad=copy.deepcopy(q);bad['outcomes']=[{'stage':ORDER[0],'outcome':'normal'}];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('unsupported normal finalizer join '+str(term),bad)
  for i,stage in enumerate(ORDER):
   bad=copy.deepcopy(fx);del bad['outcomes'][i];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('missing '+stage,bad)
   bad=copy.deepcopy(fx);bad['outcomes'].insert(i,copy.deepcopy(bad['outcomes'][i]));bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('duplicated '+stage,bad)
  for order in itertools.permutations(ORDER):
   if list(order)==ORDER:continue
   bad=copy.deepcopy(fx);bad['outcomes']=[{'stage':v,'outcome':'normal'} for v in order];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('reordered '+str(order),bad)
  for path,value in [(('invocation',),'different'),(('context',),'SYMBOLIC-U-TWO' if idx==0 else 'SYMBOLIC-U-ONE'),(('anchor','instance','binding'),'0'*64),(('exit_case','invocation'),'different'),(('projection','descriptor','scope','acquisition'),'other-acquisition'),(('projection','descriptor','scope','instance','ownership_incarnation'),'0'*64),(('projection','descriptor','owner_lock_occurrence'),'other/owner-lock'),(('projection','descriptor','descriptor_result_occurrence'),'other/owner-lock/os.open-result'),(('projection','descriptor','slot'),'other_fd'),(('projection','descriptor','producer','site'),'1:0:1:1:Call'),(('projection','descriptor','close_argument_origin','expression'),'other_fd'),(('projection','descriptor','lock_path','nominal_recorded_path'),'/wrong/.owner.lock'),(('projection','descriptor','lock_path','physical_resolved_path'),'/invented'),(('projection','descriptor','numeric_value'),8),(('projection','descriptor','physical_resource_identity'),'inode:123'),(('projection','references','manager','symbol'),'other-manager'),(('projection','references','session','symbol'),'other-wrapper'),(('projection','session_binding','recorded_destination'),'/foreign')]:reject('wrong binding '+str(path),change(fx,path,value))
  other=case(m,b,idx,inv='review-owner-002');accept('repeated equal operation with new invocation',other)
  rec.check(tag+' distinct descriptor occurrence and event identity',lambda:fx['output']['descriptor_lineage']['descriptor_result_occurrence']!=other['output']['descriptor_lineage']['descriptor_result_occurrence'] and {e['id'] for e in fx['output']['events']}.isdisjoint(e['id'] for e in other['output']['events']))
  for label,replacement in [('foreign projections',other),('other context',case(m,b,1-idx))]:
   bad=copy.deepcopy(fx);bad['projection']=copy.deepcopy(replacement['projection']);bad['output']=copy.deepcopy(replacement['output']);reject('coordinated '+label,bad)
  bad=copy.deepcopy(fx);bad['exit_case']=copy.deepcopy(other['exit_case']);reject('foreign actual predecessor',bad)
  bad=copy.deepcopy(fx);bad['projection']['descriptor']['numeric_value']=8;bad['output']['descriptor_lineage']=copy.deepcopy(bad['projection']['descriptor'])
  for event in bad['output']['events']:event['descriptor']=copy.deepcopy(bad['projection']['descriptor'])
  reject('coordinated invented numeric descriptor',bad)
  bad=copy.deepcopy(fx);bad['projection']['descriptor']=8;bad['output']['descriptor_lineage']=8;reject('bare descriptor number not lineage',bad)
  bad=copy.deepcopy(fx);bad['projection']['exit_result']['marker_removal_completed_in_model']=False;bad['output']['validated_normal_exit_prefix']=copy.deepcopy(bad['projection']['exit_result']);reject('coordinated changed predecessor',bad)
  for field in ('physical_descriptor_closure_established','physical_lock_release_established','exclusive_ownership_established','durability_established','complete_outer_context_exit_established','obligations_discharged','authorization_renewed','actual_admission'):
   reject('unsupported conclusion '+field,change(fx,('output',field),True))
  for field,value in [('descriptor_close_return_observation',None if False else 0),('runtime_descriptor_finalization',[]),('observer_join',{}),('retained_error',{}),('exceptional_outer_cleanup_completion',True)]:reject('unobserved output '+field,change(fx,('output',field),value))
  for path,T in [(('invocation',),S),(('outcomes',),L),(('projection','descriptor'),D),(('projection','descriptor','slot'),S),(('projection','descriptor','source','bytes'),I),(('output','events'),L),(('output','completion'),S)]:
   v=fx
   for k in path:v=v[k]
   reject('exact type '+str(path),change(fx,path,T(v)))
  bad=copy.deepcopy(fx);bad['output']['descriptor_lineage']={S(k):v for k,v in bad['output']['descriptor_lineage'].items()};reject('nested literal-key subclass',bad)
  for field in ('normal_route_applicable','finalizer_entry_completed_in_model','descriptor_close_attempt_entered_in_model','descriptor_close_normal_completion_in_model'):reject('integer instead of boolean '+field,change(fx,('output',field),1))
  bad=copy.deepcopy(fx);bad['outcomes'][0]['outcome']='interrupted';bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);reject('undeclared outcome cannot silently normalize',bad)
  out=m._construct_checked(b,fx);out['projection']['descriptor_lineage']['scope']['instance'].clear();out['projection']['events'][0]['descriptor']['source'].clear();out['projection']['validated_normal_exit_prefix']['reference_bindings'].clear();out['anchor'].clear();accept('nested returned mutations leave expectations pristine',fx)
  descriptor=c.owner_descriptor_lineage(cat,fx['projection']['scope'],fx['projection']['session_binding'],fx['projection']['marker_path']);descriptor['producer'].clear();descriptor['scope']['instance'].clear();rec.check(tag+' lineage copy isolation',lambda:c.owner_descriptor_lineage(cat,fx['projection']['scope'],fx['projection']['session_binding'],fx['projection']['marker_path'])==fx['projection']['descriptor'])
  v=m._premises(b,fx);rec.check(tag+' direct semantic projection accepts validated premises',lambda:c.validate_owner_finalization_projection(cat,fx['projection'],v,fx['output']))
  rec.reject(tag+' direct output stale descriptor',lambda:c.validate_owner_finalization_projection(cat,fx['projection'],v,change(fx['output'],('descriptor_lineage','descriptor_result_occurrence'),'stale')))
  for path,value in [(('conditional_links',),[]),(('descriptor_lineage','numeric_value'),8),(('descriptor_lineage','owner_lock_occurrence'),'invented'),(('runtime_finalizer_chain',),[]),(('classification',),'QUALIFIED'),(('multiplicity',),0)]:
   bad=copy.deepcopy(rows);q=bad[idx]
   for k in path[:-1]:q=q[k]
   q[path[-1]]=value;rec.reject(tag+' semantic claim '+str(path),lambda bad=bad:m._check_rows(b,bad))
 for label,edit in [('missing stage',lambda x:x['declarations'].pop()),('missing guard',lambda x:x['guard_branches'].pop('ordered_normal_prefix')),('different close argument',lambda x:x['source'].update(close_arguments=['other_fd'])),('missing fd declaration',lambda x:x['descriptor_declaration'].clear()),('weakened order',lambda x:x['source']['order'].reverse())]:
  bad=copy.deepcopy(cat);edit(bad);rec.reject('source oracle rejects '+label,lambda bad=bad:c.validate_owner_finalization(m.sources(data)[0],m.dependency(data),bad))
 # Alter both proposed source bytes and their claimed dependent identity: source shape still rejects.
 raw=m.sources(data)[0]
 for old,new in [(b'finally:os.close(fd)',b'finally:os.close(fd+1)'),(b'finally:os.close(fd)',b'finally:pass'),(b'0o600)',b'0o666)')]:
  changed_raw=raw.replace(old,new);rec.check('source mutation non-noop '+new.decode(),lambda changed_raw=changed_raw:changed_raw!=raw);dep=copy.deepcopy(m.dependency(data));dep['source']['launcher']=ident(changed_raw);rec.reject('coordinated source and pin alteration '+new.decode(),lambda changed_raw=changed_raw,dep=dep:c.compile_owner_finalization(changed_raw,dep))
 for candidate in [[],list(reversed(rows)),[rows[0],rows[0]]]:rec.reject('semantic exact context domain '+str(len(candidate)),lambda candidate=candidate:m._check_rows(b,candidate))
 for key in ['evidence/confirmed-close.json','evidence/session-records/binding.json']:
  e=dict(b['evidence']);e.pop(key);rec.reject('missing current evidence '+key,lambda e=e:m._compare_evidence(b,e))
 e=dict(b['evidence']);e['evidence/confirmed-close.json']+=b' ';rec.reject('altered actual evidence bytes',lambda:m._compare_evidence(b,e))
 out=m._assemble(data,rows,b);out['contexts'].reverse();out['contexts'][0]['owner_lock_finalization_correspondence']['descriptor_lineage'].clear();out['extension_components'].clear();rec.check('bundle reversal and nested aliases isolated',lambda:enc(m._assemble(data,rows,b))==saved)
 rec.check('obligations UNKNOWNs and observer preserved',lambda:bundle['unchanged_obligations']==b['prior']['unchanged_obligations'] and bundle['inventory_unknown_totals']==4 and bundle['lifetime_unknown_totals']==14 and all(r['observer_join'] is None and r['numeric_descriptor_observation'] is None for r in rows))
 rec.save('independent-fixtures.json',{'cases':fixtures});rec.save('receipt-identity.json',ident(saved));rec.save('final-root-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Fresh independent owner-lock descriptor-finalization controls only')
