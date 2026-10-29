"""Reviewer-owned source traversal, independent case inputs and milestone oracle."""
import ast,copy,hashlib,inspect,pathlib
from common import enc,ident
ORDER=['session-resume','launcher-resume','close-attempt','close-complete','managed-clear','unlink-attempt','unlink-complete']
TOKEN=['owner-create','token-create','registry-insert','control-guard','control-create','control-callback','client-create','client-callback','owner-failure-guard','finally-enter','removal-attempt','removal-complete']
def source_checks(m,data,cat):
 launcher,entry,manager=m.sources(data);lt,et,mt=[ast.parse(x) for x in (launcher,entry,manager)]
 def fn(t,name):return next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name==name)
 f=fn(lt,'_session');yieldnode=next(n for n in ast.walk(f) if isinstance(n,ast.Expr) and isinstance(n.value,ast.Yield));tr=next(n for n in ast.walk(f) if isinstance(n,ast.Try) and yieldnode in n.body);idx=tr.body.index(yieldnode)
 tail=tr.body[idx:];assert [ast.unparse(x) for x in tail]==['yield ManagedSession(managed)','managed.close()','managed = None',"(dest / 'ACTIVE.json').unlink()"]
 assert len(tr.handlers)==1 and ast.unparse(tr.handlers[0].type)=='BaseException' and not tr.finalbody
 close,clear,unlink=tail[1:];assert not unlink.value.args and not unlink.value.keywords
 bridge=fn(lt,'session').body[-1];assert ast.unparse(bridge)=='with _session(*args, **kwargs) as managed:\n    yield managed'
 run=fn(et,'_run');rw=next(n for n in ast.walk(run) if isinstance(n,ast.With));assert ast.unparse(rw.items[0].context_expr)=='launcher.session(candidate, draft, runtime, destination, create=create)'
 pop=next(n for n in ast.walk(run) if isinstance(n,ast.Call) and ast.unparse(n.func)=='_OWNERS.pop');assert ast.unparse(pop)=='_OWNERS.pop(token, None)'
 nodes=[bridge.body[0],yieldnode,close.value,close,clear,unlink.value,unlink]
 assert cat['source']['order']==ORDER and [d['id'] for d in cat['declarations']]==ORDER
 for label,n in zip(ORDER,nodes):
  origin=cat['source']['stages'][label];assert origin['site']==f'{n.lineno}:{n.col_offset}:{n.end_lineno}:{n.end_col_offset}:{type(n).__name__}'
  assert origin['expression']==ast.get_source_segment(launcher.decode(),n) and origin['source']==ident(launcher)
  assert next(d for d in cat['declarations'] if d['id']==label)['source_origin']==origin
  expected_guards=[{'contexts':['_session(*args, **kwargs)'],'kind':'with'}] if label=='session-resume' else [{'contexts':['owner_lock(destination)'],'kind':'with'},{'handlers':['BaseException'],'kind':'try','region':'body'}]
  assert origin['guards']==expected_guards
  if label!='session-resume':
   statement=n if n in tr.body else next(s for s in tr.body if n in list(ast.walk(s)))
   expected_prefix=[f'{s.lineno}:{s.col_offset}:{s.end_lineno}:{s.end_col_offset}:{type(s).__name__}' for s in tr.body[:tr.body.index(statement)]]
   assert [x['site'] for x in origin['continuation'][-1]['normal_prefix']]==expected_prefix
 managed=next(n for n in mt.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');mc=fn(managed,'close')
 assert [ast.unparse(n) for n in mc.body[0].body]==["self._quarantine('explicit close')",'self._dispose()',"self._phase = 'CLOSED'","self._reason = 'close confirmed; no serving connection'"]
 lock=fn(lt,'owner_lock');locktext=ast.unparse(lock);assert 'parent = dest.parent.resolve()' in locktext and 'dest = parent / dest.name' in locktext and 'yield dest' in locktext
 std=inspect.getsource(pathlib.Path.unlink);st=ast.parse(inspect.cleandoc(std));sf=st.body[0]
 assert ast.literal_eval(sf.args.kw_defaults[0]) is False and 'except FileNotFoundError:' in std and 'if not missing_ok:' in std
 return {'stage_sites':{n:cat['source']['stages'][n]['site'] for n in ORDER},'launcher':ident(launcher),'entry':ident(entry),'manager':ident(manager),'Path.unlink_source':std,'Path.unlink_source_identity':ident(std.encode()),'normal_tail': [ast.unparse(n) for n in tail],'exception_handler':ast.get_source_segment(launcher.decode(),tr.handlers[0]),'owner_lock':ast.get_source_segment(launcher.decode(),lock)}
def token_case(m,b,idx,inv,control=True,continuity=True,terminal=None,owner_none=True):
 tb=b['token_basis'];anchor=copy.deepcopy(m._rows(b)[idx]['instance_anchor'])
 scope={'context':anchor['context'],'acquisition':anchor['record']['acquisition'],'instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence'],'invocation':inv}
 outcomes=[]
 for stage in TOKEN:
  if not control and stage in ('control-create','control-callback'):continue
  kind=terminal[1] if terminal and terminal[0]==stage else 'normal';outcomes.append({'stage':stage,'outcome':kind})
  if kind!='normal' or stage=='owner-failure-guard' and not owner_none:break
 v={'occurrence':inv,'scope':scope,'control_present':control,'owner_failure_none':owner_none,'registry_continuity':continuity,'outcomes':outcomes}
 c=b['fresh']['prior_module'];producer=tb['fresh']['coverage'];refs={n:{'scope':copy.deepcopy(scope),'symbol':inv+'/'+n+'-symbol'} for n in ('token','owner','session','manager','client')};refs['control']={'scope':copy.deepcopy(scope),'symbol':inv+'/control-symbol'} if control else None
 refs.update({'client.token':copy.deepcopy(refs['token']),'control.token':copy.deepcopy(refs['token']) if control else None,'owners[token]':copy.deepcopy(refs['owner']),'owner.wrapper':copy.deepcopy(refs['session']),'session.managed':copy.deepcopy(refs['manager'])})
 p={**copy.deepcopy(v),'references':refs};out=producer.token_registration_projection(tb['catalogue'],p,v)
 return {'kind':'CONSTRUCTED-TOKEN-REGISTRATION','context':anchor['context'],'anchor':anchor,'invocation':inv,**{k:copy.deepcopy(v[k]) for k in ('control_present','owner_failure_none','registry_continuity','outcomes')},'projection':p,'output':out}
def case(m,b,idx=0,inv='review-exit-001',control=True,continuity=True,terminal=None,marker='UNKNOWN',initial=None,token_terminal=None,owner_none=True,close_outcomes=None,stop_after=None):
 tc=token_case(m,b,idx,inv,control,continuity,token_terminal,owner_none);anchor=tc['anchor'];outcomes=[]
 if tc['output']['completion']=='normal-pop-completion':
  for stage in ORDER:
   kind=terminal[1] if terminal and terminal[0]==stage else 'normal';outcomes.append({'stage':stage,'outcome':kind})
   if kind!='normal':break
 reached=next((e for e in outcomes if e['stage']=='close-complete'),None)
 cs={'acquisition':anchor['record']['acquisition'],'instance':'validated-instance:'+hashlib.sha256(enc(anchor['instance'])).hexdigest(),'invocation':inv+'/managed-close'}
 cc=None
 if reached and (reached['outcome'] not in ('unobserved','process-termination') or stop_after is not None or close_outcomes):
  cc={'kind':'CONSTRUCTED-REFERENCE-PATH','context':anchor['context'],'scope':cs,'method':'close','initial':initial or {'_live':'review-connection','_retired':None,'_phase':'READY'},'facts':{},'outcomes':close_outcomes or {},'stop_after':stop_after}
 q={'kind':'CONSTRUCTED-NORMAL-SESSION-EXIT','context':anchor['context'],'anchor':copy.deepcopy(anchor),'invocation':inv,'token_case':tc,'close_case':cc,'outcomes':outcomes,'marker_at_unlink':marker,'projection':{},'output':{}}
 return refresh(m,b,q)
def refresh(m,b,q):
 v=m._premises(b,q);q['projection']=copy.deepcopy(v);q['output']=b['fresh']['coverage'].session_exit_projection(b['catalogue'],q['projection'],v);return q
def check_model(q):
 """Independently calculate acknowledged-prefix milestones from supplied premises."""
 out=q['output'];normal=q['token_case']['output']['completion']=='normal-pop-completion';assert out['validated_token_prefix']==q['token_case']['output']
 done=[];stages=[];terminal=None
 if normal:
  for expected,row in zip(ORDER,q['outcomes']):
   assert row['stage']==expected;stages.append(expected);terminal=row['outcome']
   if terminal!='normal':break
   done.append(expected)
 assert len(stages)==len(q['outcomes']) and [e['stage'] for e in out['events']]==stages
 for key,stage in [('close_attempt_entered_in_model','close-attempt'),('close_normal_completion_in_model','close-complete'),('launcher_local_cleared_in_model','managed-clear'),('unlink_attempt_entered_in_model','unlink-attempt'),('marker_removal_completed_in_model','unlink-complete')]:assert out[key] is (stage in done)
 assert out['launcher_local_managed_after']==(None if 'managed-clear' in done else out['reference_bindings']['manager'])
 assert out['wrapper_manager_reference_after']==out['reference_bindings']['manager']
 for e in out['events']:
  assert e['scope']==out['scope'] and e['id']==q['invocation']+'/'+e['stage'] and e['manager']==out['reference_bindings']['manager'] and e['wrapper']==out['reference_bindings']['session'] and e['runtime_frame'] is None
 for key in ('physical_closure_established','durability_established','runtime_exclusivity_established','outer_context_exit_or_lock_release_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission','runtime_observation'):assert out[key] is False
 for key in ('marker_absence_persists','runtime_exit_chain','outer_cleanup_completion','retained_error','observer_join'):assert out[key] is None
 assert out['terminal_python_exception_in_model'] is (True if terminal in ('raise','missing-file') else False if terminal=='normal' else None)
 if terminal=='missing-file':assert out['exception_class']=='FileNotFoundError' and out['marker_namespace_fact']=='ABSENT-REPORTED-BY-UNLINK' and out['marker_removal_completed_in_model'] is False
 elif 'unlink-complete' in done:assert out['marker_namespace_fact']=='ABSENT-AT-UNLINK-COMPLETION'
 else:assert out['marker_namespace_fact']=='UNKNOWN'
 return True
def changed(v,path,value):
 q=copy.deepcopy(v);p=q
 for k in path[:-1]:p=p[k]
 p[path[-1]]=value;return q
