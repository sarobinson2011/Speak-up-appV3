"""New conditional cases using exact saved predecessor cases, not runtime observations."""
import copy,json,ast
from pathlib import Path
D=copy.deepcopy
def outcomes(cat,frontier=None):
 out=[]
 for s in cat['source']['steps']:
  out.append({'stage':s['id'],'outcome':frontier[1] if frontier and frontier[0]==s['id'] else s['normal_outcome']})
  if frontier and frontier[0]==s['id']:break
 return out
def make(m,cat,parent_case,session,continuity='explicit conditional premise',frontier=None):
 p=D(parent_case['output']);anchor=D(parent_case['anchor']);c=m['coverage'];b=c.write_call_binding(cat,p,anchor,session,continuity)
 if continuity=='UNESTABLISHED':frontier=(cat['source']['order'][0],'unobserved')
 v={'scope':D(p['scope']),'anchor':anchor,'parent_result':p,'session_binding':D(session),'binding':b,'outcomes':outcomes(cat,frontier)}
 return {'kind':'CONSTRUCTED-WRITE-CALL-REPLACEMENT','context':parent_case['context'],'anchor':D(anchor),'invocation':parent_case['invocation'],'parent_case':D(parent_case),'parent_output':D(p),'session_binding':D(session),'binding':D(b),'outcomes':D(v['outcomes']),'projection':v,'output':c.write_call_projection(cat,v,v)}
def oracle(out,parent,normal=True,terminal=None):
 assert out['original_error_pending_in_outer_handler']==parent['original_error_pending_in_outer_handler']
 assert out['cleanup_list_state']==parent['cleanup_list_state'] and out['known_false_flags_preserved']==parent['known_false_flags_preserved']
 assert out['close_normal_return_completed_in_model']==parent['close_normal_return_completed_in_model'] and out['failure_origin_region']==parent['failure_origin_region']
 for k in ('pid_value','directory_count_value','filename_value','exact_path_value','runtime_chain','observer_join'):assert out[k] is None
 for k in ('write_new_body_entry_established','write_new_return_established','file_open_established','file_write_established','file_flush_established','file_fsync_established','line175_suppression_established','final_rethrow_established','owner_finalization_established','normal_overall_return_established','physical_closure_established','actual_admission'):assert out[k] is False
 assert out['call_attempt_established'] is normal
 assert out['terminal_python_exception_in_model'] is (None if terminal in ('unobserved','process-termination') else True)
 if normal:assert out['last_pending_error_in_model']==parent['original_error_pending_in_outer_handler'] and out['replacement_error_in_model'] is None
 elif terminal in ('raise','catchable-interruption'):assert out['replacement_error_in_model'] is not None and out['last_pending_error_in_model']==out['replacement_error_in_model']
 return True
def source_oracle(raw):
 # Independent traversal: explicit Python field order; ignores generated catalogue.
 t=ast.parse(raw);fn=next(x for x in t.body if isinstance(x,ast.FunctionDef) and x.name=='_session');handler=fn.body[-1].body[-1].handlers[0];reg=handler.body[2];root=reg.body[0].value
 assert reg.lineno==174 and isinstance(root.func,ast.Name) and root.func.id=='write_new' and len(root.args)==2 and not root.keywords
 assert isinstance(root.args[1],ast.Name) and root.args[1].id=='details'
 result=[('explicit continuation into selected protecting try',reg)]
 def walk(n):
  if isinstance(n,ast.Name):result.append(('name lookup',n))
  elif isinstance(n,ast.Constant):assert type(n.value) is str;result.append(('literal',n))
  elif isinstance(n,ast.Attribute):walk(n.value);result.append(('attribute lookup',n))
  elif isinstance(n,ast.BinOp):walk(n.left);walk(n.right);result.append(('binary operation',n))
  elif isinstance(n,ast.Call):
   walk(n.func)
   for a in n.args:walk(a)
   result.extend([('nested call attempt',n),('nested normal return',n)])
  else:raise AssertionError(type(n).__name__)
 walk(root.func)
 for a in root.args:walk(a)
 result.append(('write_new call attempt; body excluded',root))
 return [(op,[n.lineno,n.col_offset,n.end_lineno,n.end_col_offset,type(n).__name__]) for op,n in result]
