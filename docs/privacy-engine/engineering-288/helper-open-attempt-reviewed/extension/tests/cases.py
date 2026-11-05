"""Focused new source oracle and conditional cases; no runtime observations."""
import ast,copy
D=copy.deepcopy
def plan(raw):
 t=ast.parse(raw);f=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='write_new');s=next(n for n in t.body if isinstance(n,ast.FunctionDef) and n.name=='_session')
 call=next(n for n in ast.walk(s) if isinstance(n,ast.Call) and n.lineno==174 and isinstance(n.func,ast.Name) and n.func.id=='write_new')
 assert [a.arg for a in f.args.args]==['p','x'] and not f.args.defaults
 w=f.body[0];assert isinstance(w,ast.With) and len(w.items)==1;c=w.items[0].context_expr
 assert c.func.id=='open' and [a.id if isinstance(a,ast.Name) else a.value for a in c.args]==['p','xb'] and not c.keywords
 def loc(n):return [n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__]
 # Source fields, not producer catalogue, determine the ordered nodes.
 return [('explicit continuation after validated call attempt',loc(call)),('conditional selected-helper entry acknowledgment',loc(f)),('source positional parameter correspondence',loc(f)),('name lookup',loc(c.func)),('parameter lookup',loc(c.args[0])),('literal',loc(c.args[1])),('open call attempt; return excluded',loc(c))]
def outcomes(cat,frontier=None):
 oo=[]
 for st in cat['source']['steps']:
  oo.append({'stage':st['id'],'outcome':frontier[1] if frontier and frontier[0]==st['id'] else st['normal_outcome']})
  if frontier and frontier[0]==st['id']:break
 return oo
def make(c,cat,pc,continuity='explicit conditional premise',frontier=None):
 p=D(pc['output']);a=D(pc['anchor']);b=c.helper_open_binding(cat,p,a,continuity)
 if continuity=='UNESTABLISHED':frontier=(cat['source']['order'][0],'unobserved')
 v={'scope':D(p['scope']),'anchor':D(a),'parent_result':D(p),'binding':D(b),'outcomes':outcomes(cat,frontier)}
 return {'kind':'CONSTRUCTED-HELPER-OPEN-ATTEMPT','context':pc['context'],'anchor':a,'invocation':pc['invocation'],'parent_case':D(pc),'parent_output':D(p),'binding':b,'outcomes':D(v['outcomes']),'projection':v,'output':c.helper_open_projection(cat,v,v)}
EXCLUDED=('open_return_established','file_creation_established','context_manager_entry_established','f_binding_established','encoding_established','file_write_established','file_flush_established','file_fsync_established','context_manager_exit_established','helper_return_established','failure_file_established','line175_handler_entry_established','line175_suppression_established','final_rethrow_established','owner_finalization_established','managed_local_clear_established','active_removal_established','complete_cleanup_established','normal_overall_return_established','physical_closure_established','durability_established','released_ownership_established','obligations_discharged','external_nonexecution_established','authorization_renewed','actual_admission')
def oracle(out,parent,stage=None,terminal=None):
 normal=terminal is None
 assert out['open_call_attempt_established_in_model'] is normal
 assert out['terminal_python_exception_in_model'] is (None if terminal in ('process-termination','unobserved') else True)
 assert all(out[k] is False for k in EXCLUDED)
 for k in ('pid_value','directory_count_value','filename_value','exact_path_value','physical_reference_identity','runtime_chain','observer_join'):assert out[k] is None
 for k in ('original_error_pending_in_outer_handler','cleanup_list_state','known_false_flags_preserved','failure_origin_region','close_normal_return_completed_in_model','retained_cleanup_error_evidence'):assert out[k]==parent[k]
 if terminal in ('raise','catchable-interruption'):
  assert out['replacement_error_in_model']['origin']==out['events'][-1]['source']
  assert out['last_pending_error_in_model']==out['replacement_error_in_model']
 else:assert out['last_pending_error_in_model']==parent['original_error_pending_in_outer_handler'] and out['replacement_error_in_model'] is None
 if normal:
  assert out['helper_entry_established_in_model'] is True and out['parameter_binding_established_in_model'] is True
  assert out['bound_parameters']['p']['argument']==parent['call_arguments']['p']
  assert out['bound_parameters']['x']['argument']==parent['call_arguments']['x']==parent['binding']['details_role']
  assert out['open_arguments']['mode']['concrete_value']=='xb' and type(out['open_arguments']['mode']['concrete_value']) is str
  assert out['open_arguments']['p']['bound_role']==out['bound_parameters']['p']
 else:
  index=['open:continuation','open:helper-entry','open:parameters','open:callable','open:path','open:mode','open:attempt'].index(stage)
  assert out['helper_entry_established_in_model'] is (index>1)
  assert out['parameter_binding_established_in_model'] is (index>2)
  assert len(out['events'])==index+1
 return True
