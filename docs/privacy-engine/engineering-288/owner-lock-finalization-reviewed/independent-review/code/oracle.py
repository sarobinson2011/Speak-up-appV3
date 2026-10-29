"""Formal-Lab[6] source traversal, fresh premises and independent milestone oracle."""
import ast,copy
from pathlib import PurePosixPath
from common import enc,ident
import exit_fixture
ORDER=['owner-finalizer-enter','descriptor-close-attempt','descriptor-close-complete']
def site(n):return f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}'
def source_check(m,data,cat):
 raw=m.sources(data)[0];tree=ast.parse(raw);functions={n.name:n for n in tree.body if isinstance(n,ast.FunctionDef)};lock=functions['owner_lock'];launch=functions['_session']
 stores=[n for n in ast.walk(lock) if isinstance(n,ast.Name) and n.id=='fd' and isinstance(n.ctx,(ast.Store,ast.Del))];assert len(stores)==1 and isinstance(stores[0].ctx,ast.Store)
 alloc=next(n for n in lock.body if isinstance(n,ast.Assign) and stores[0] in n.targets);opening=alloc.value;tr=next(n for n in lock.body if isinstance(n,ast.Try) and n.finalbody)
 assert lock.body.index(alloc)<lock.body.index(tr) and not tr.handlers and not tr.orelse
 assert isinstance(opening,ast.Call) and ast.unparse(opening.func)=='os.open' and len(opening.args)==3 and not opening.keywords
 path,flags,mode=opening.args;assert ast.unparse(path)=="parent / ('.' + dest.name + '.owner.lock')" and ast.unparse(flags)=='os.O_CREAT | os.O_RDWR | os.O_NOFOLLOW' and ast.literal_eval(mode)==0o600
 assert len(tr.finalbody)==1;close=tr.finalbody[0];assert isinstance(close,ast.Expr) and isinstance(close.value,ast.Call) and ast.unparse(close.value)=='os.close(fd)' and not close.value.keywords
 assert len(close.value.args)==1 and isinstance(close.value.args[0],ast.Name) and close.value.args[0].id==alloc.targets[0].id=='fd'
 yield_=next(n for n in tr.body if isinstance(n,ast.Expr) and isinstance(n.value,ast.Yield));assert ast.unparse(yield_)=='yield dest' and tr.body[-1] is yield_
 flock=next(n for n in ast.walk(tr.body[0]) if isinstance(n,ast.Call) and ast.unparse(n.func)=='fcntl.flock');assert [ast.unparse(x) for x in flock.args]==['fd','fcntl.LOCK_EX | fcntl.LOCK_NB']
 innertry=tr.body[0];assert len(innertry.handlers)==1 and ast.unparse(innertry.handlers[0].type)=='BlockingIOError' and ast.unparse(innertry.handlers[0].body[0])=="raise Blocked('OWNER-LOCK-CONTENDED')"
 outer=next(n for n in launch.body if isinstance(n,ast.With) and ast.unparse(n.items[0].context_expr)=='owner_lock(destination)');assert launch.body[-1] is outer and ast.unparse(outer.items[0].optional_vars)=='dest'
 tailtry=outer.body[-1];assert isinstance(tailtry,ast.Try) and not tailtry.orelse and not tailtry.finalbody
 tail=tailtry.body[-1];assert ast.unparse(tail)=="(dest / 'ACTIVE.json').unlink()" and [ast.unparse(n) for n in tailtry.body[-3:]]==['managed.close()','managed = None',"(dest / 'ACTIVE.json').unlink()"]
 source=cat['source'];assert source['order']==ORDER and [x['id'] for x in cat['declarations']]==ORDER
 for key,n in [('descriptor_assignment',alloc),('descriptor_call',opening),('close_argument',close.value.args[0]),('owner_lock_call',outer.items[0].context_expr),('yield',yield_),('normal_predecessor',tail)]:
  origin=source[key];assert origin['site']==site(n) and origin['expression']==ast.get_source_segment(raw.decode(),n)
 for label,n in zip(ORDER,[tr,close.value,close]):
  origin=source['stages'][label];assert origin['site']==site(n) and origin['expression']==ast.get_source_segment(raw.decode(),n) and origin['source']==ident(raw)
  expected=[] if label=='owner-finalizer-enter' else [{'handlers':[],'kind':'try','region':'finalbody'}];assert origin['guards']==expected
  assert origin['semantic_region']==('finally-entry' if label=='owner-finalizer-enter' else 'finalbody')
  assert next(x for x in cat['declarations'] if x['id']==label)['source_origin']==origin
  prefix=origin['continuation'][0]['normal_prefix'];assert [x['site'] for x in prefix]==[site(x) for x in lock.body[:lock.body.index(tr)]]
  if label!='owner-finalizer-enter':assert origin['continuation'][-1]['region']=='finalbody' and origin['continuation'][-1]['normal_prefix']==[]
 assert source['open_arguments']==[ast.unparse(x) for x in opening.args] and source['close_callee']=='os.close' and source['close_arguments']==['fd'] and source['close_keywords']==[]
 assert source['path_prefix']=='.' and source['path_suffix']=='.owner.lock' and cat['descriptor_declaration']['slot']=='fd'
 return {'source':ident(raw),'owner_lock_source':ast.get_source_segment(raw.decode(),lock),'single_fd_assignment':site(alloc),'os_open_call':site(opening),'guarded_yield':site(yield_),'flock_call':site(flock),'stages':{label:site(n) for label,n in zip(ORDER,[tr,close.value,close])},'normal_predecessor':site(tail),'open_arguments':source['open_arguments'],'close_arguments':['fd'],'model_entry_marker_is_containing_try_anchor_not_observed_finally_event':True,'no_runtime_or_filesystem_operation':True}
def case(m,b,idx=0,inv='review-owner-001',continuity=True,terminal=None,exit_terminal=None,marker='UNKNOWN',control=True):
 p=b['fresh']['prior_module'];ec=exit_fixture.case(p,b['exit_basis'],idx,inv=inv,continuity=continuity,terminal=exit_terminal,marker=marker,control=control)
 outcomes=[]
 if ec['output']['completion']=='normal-marker-unlink-completion':
  for stage in ORDER:
   kind=terminal[1] if terminal and terminal[0]==stage else 'normal';outcomes.append({'stage':stage,'outcome':kind})
   if kind!='normal':break
 q={'kind':'CONSTRUCTED-OWNER-LOCK-FINALIZATION','context':ec['context'],'anchor':copy.deepcopy(ec['anchor']),'invocation':inv,'exit_case':ec,'outcomes':outcomes,'projection':{},'output':{}}
 return refresh(m,b,q)
def refresh(m,b,q):
 v=m._premises(b,q);q['projection']=copy.deepcopy(v);q['output']=b['fresh']['coverage'].owner_finalization_projection(b['catalogue'],q['projection'],v);return q
def check_model(q):
 out=q['output'];prior=q['exit_case']['output'];assert out['validated_normal_exit_prefix']==prior
 normal=prior['completion']=='normal-marker-unlink-completion' and prior['marker_removal_completed_in_model'] is True;assert out['normal_route_applicable'] is normal
 stages=[];done=[];terminal=None
 if normal:
  for stage,row in zip(ORDER,q['outcomes']):
   assert row['stage']==stage;stages.append(stage);terminal=row['outcome']
   if terminal!='normal':break
   done.append(stage)
 assert len(stages)==len(q['outcomes']) and [e['stage'] for e in out['events']]==stages
 for field,stage in [('finalizer_entry_completed_in_model',ORDER[0]),('descriptor_close_attempt_entered_in_model',ORDER[1]),('descriptor_close_normal_completion_in_model',ORDER[2])]:assert out[field] is (stage in done)
 assert out['terminal_python_exception_in_model'] is (True if terminal=='raise' else False if terminal=='normal' else None)
 assert out['selected_owner_removed_in_model'] is prior['selected_owner_removed_in_model'] and out['continuity_premise']==prior['continuity_premise']
 desc=out['descriptor_lineage'];scope=prior['scope'];assert out['scope']==scope and desc['scope']==scope
 assert desc['owner_lock_occurrence']==q['invocation']+'/owner-lock' and desc['descriptor_result_occurrence']==q['invocation']+'/owner-lock/os.open-result' and desc['slot']=='fd'
 nominal=PurePosixPath(prior['session_binding']['recorded_destination']);expected=str(nominal.parent/('.'+nominal.name+'.owner.lock'));assert desc['lock_path']['nominal_recorded_path']==expected and desc['lock_path']['physical_resolved_path'] is None
 for field in ('numeric_value','runtime_descriptor_identity','physical_resource_identity'):assert desc[field] is None
 assert desc['exclusive_owner_established'] is False
 for e in out['events']:
  assert e['id']==q['invocation']+'/'+e['stage'] and e['scope']==scope and e['descriptor']==desc and e['descriptor_result_occurrence']==desc['descriptor_result_occurrence'] and e['manager']==prior['reference_bindings']['manager'] and e['session']==prior['reference_bindings']['session'] and e['runtime_frame'] is None
 for field in ('physical_descriptor_closure_established','physical_lock_release_established','exclusive_ownership_established','durability_established','complete_outer_context_exit_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission','runtime_observation'):assert out[field] is False
 for field in ('runtime_descriptor_finalization','exceptional_outer_cleanup_completion','retained_error','observer_join','descriptor_close_return_observation'):assert out[field] is None
 assert out['runtime_unwind_evidence']=='UNAVAILABLE'
 if not normal:assert out['completion']=='outside-normal-finalization-slice'
 elif terminal=='normal':assert out['completion']=='normal-descriptor-close-completion'
 return True
def change(v,path,value):
 q=copy.deepcopy(v);p=q
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return q
