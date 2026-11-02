"""Independent EC-01 controls using only the live actual public-returned basis.
No Engineering oracle/factory is imported. Prior independent constructors are
reused to supply unchanged prerequisites; only the corrected slice is tested.
"""
from common import *
from cases import build,oracle,ORDER
import ast
class S(str):pass
class Dct(dict):pass
def run(m,b,public,saved,r):
 layer='actual-authenticated-basis _construct_checked and output-comparison core'
 layers=[]
 def yes(name,fn,where=layer):
  v=r.yes(name,fn);layers.append({'check':name,'layer':where,'result':'PASS'});return v
 def no(name,fn,code='CLEANUP-OUTPUT-CORRESPONDENCE',where=layer):
  r.no(name,fn,code);layers.append({'check':name,'layer':where,'result':'REJECTED'})
 root=b['fresh']['root'];raw=(root/'source-evidence/lab_bootstrap.py').read_bytes();tree=ast.parse(raw);fn=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_session');handler=fn.body[-1].body[-1].handlers[0];details,loop=handler.body[:2];protected=loop.body[0].body[0]
 yes('independent source: active constructor handler and normal suboperations',lambda:handler.lineno==167 and handler.name=='e' and ast.unparse(handler.type)=='BaseException' and details.lineno==168 and loop.lineno==169 and [ast.unparse(n) for n in protected.body]==['obj.close()',"details['cleanup'].append([name, 'close returned'])"] and not any(isinstance(n,(ast.Return,ast.Raise)) for n in ast.walk(loop.body[0].body[0].body[0])),'defining-source AST, not execution')
 source={'source':identity(raw),'region':'lab_bootstrap.py:167-171','normal':'True; original pending constructor error remains active','replacement_raise':'True; last pending is replacement and original provenance remains separately retained','termination_or_unobserved':'None; no new Python exception/unwind/completion inferred','line172_expanded':False,'normal_overall_return_established':False,'final_rethrow_established':False,'author_oracle_executed':False};r.save('independent-source-expectations.json',source)
 old=json.loads((root/'ec01/witnesses/EC01-smallest-case.json').read_bytes());counterpart=json.loads((root/'ec01/witnesses/EC01-source-consistent-one-field-output.json').read_bytes());corrected=D(old);corrected['output']=counterpart
 yes('retained witness counterpart changes exactly the terminal flag',lambda:set(k for k in old['output'] if old['output'][k]!=counterpart[k])=={'terminal_python_exception_in_model'} and old['output']['terminal_python_exception_in_model'] is False and counterpart['terminal_python_exception_in_model'] is True,'exact retained witness-byte comparison')
 no('retained original False witness rejected unchanged',lambda:m._construct_checked(b,old))
 yes('rejected original witness is not silently repaired',lambda:old==json.loads((root/'ec01/witnesses/EC01-smallest-case.json').read_bytes()),'submitted-object preservation after authenticated-basis rejection')
 accepted=yes('retained one-field-corrected witness accepts',lambda:m._construct_checked(b,corrected))
 yes('corrected witness obeys independent pending-exception oracle',lambda:oracle(corrected,accepted))
 r.save('retained-witness-corrected-result.json',accepted);r.save('retained-witness-corrected-case.json',corrected)
 # The original independent result remains intact; only the new result's flag differs.
 historic=json.loads((root/'ec01/witnesses/EC01-accepted-result.json').read_bytes());want=D(historic);want['projection']['terminal_python_exception_in_model']=True
 yes('new accepted witness differs from historical result in one field only',lambda:accepted==want,'exact result comparison; historical execution reused')
 normals={};frontiers=[]
 for idx in range(2):
  for control in (False,True):
   label=f'context{idx}/control{int(control)}';q=build(m,b,idx,control,invocation='fl6-ec01-'+str(idx)+'-'+str(int(control)));normals[idx,control]=q
   yes(label+' normal preserves pending original and no overall completion',lambda q=q:oracle(q,m._construct_checked(b,q)))
   for v in (False,None,1,'True'):
    bad=change(q,['output','terminal_python_exception_in_model'],v);no(label+' wrong terminal value '+repr(v),lambda bad=bad:m._construct_checked(b,bad))
   bad=D(q);del bad['output']['terminal_python_exception_in_model'];no(label+' omitted terminal classification',lambda bad=bad:m._construct_checked(b,bad))
 # Adjacent error and unknown frontiers; no line172 or later cleanup execution.
 endings=[('input-managed-object','raise','normal'),('close-normal-return','raise','abrupt'),('append-call-attempt','raise','normal'),('append-complete','raise','normal'),('close-normal-return','unobserved','partial-prefix'),('append-call-attempt','process-termination','normal'),('append-complete','unobserved','normal')]
 for idx in range(2):
  for j,(stage,outcome,close_kind) in enumerate(endings):
   q=build(m,b,idx,bool(j%2),terminal=(stage,outcome),close_kind=close_kind,invocation=f'fl6-ec01-frontier-{idx}-{j}')
   result=yes(f'context{idx} {stage}/{outcome} preserves source semantics',lambda q=q:(lambda out:(oracle(q,out),out)[1])(m._construct_checked(b,q)))
   o=result['projection'];expected=True if outcome=='raise' else None;assert o['terminal_python_exception_in_model'] is expected
   frontiers.append({'context':q['context'],'control':bool(j%2),'stage':stage,'outcome':outcome,'terminal_flag':o['terminal_python_exception_in_model'],'pending_role':o['last_pending_error_in_model']['role'],'original_retained':o['earlier_constructor_exception']==q['parent_output']['earlier_constructor_exception'],'close_return':o['close_normal_return_completed_in_model'],'append_completed':o['append_completed_in_model'],'partial_effects':o['cleanup_list_after_frontier']})
   for wrong in ([False,None] if expected is True else [False,True]):
    bad=change(q,['output','terminal_python_exception_in_model'],wrong);no(f'context{idx} {stage}/{outcome} rejects flag {wrong}',lambda bad=bad:m._construct_checked(b,bad))
   if outcome=='raise' and stage.startswith('append-'):
    bad=change(q,['output','close_normal_return_completed_in_model'],False);no(f'context{idx} append failure cannot erase acknowledged close {stage}',lambda bad=bad:m._construct_checked(b,bad))
  q=build(m,b,idx,continuity='UNESTABLISHED',invocation=f'fl6-ec01-unknown-{idx}');yes(f'context{idx} unknown continuity retains None and no progress',lambda q=q:oracle(q,m._construct_checked(b,q)))
  normal=normals[idx,False];result=m._construct_checked(b,normal);result['projection']['terminal_python_exception_in_model']=False;result['projection']['last_pending_error_in_model']['reference']='altered-return';result['projection']['details_after_acknowledged_steps']['known_literal_fields']['cleanup'].append('invented')
  yes(f'context{idx} nested returned mutations leave pristine expectations',lambda normal=normal:oracle(normal,m._construct_checked(b,normal)))
  bad=change(normal,['output','last_pending_error_in_model'],None);bad['output']['terminal_python_exception_in_model']=False;no(f'context{idx} coordinated error disappearance rejects',lambda bad=bad:m._construct_checked(b,bad))
 r.save('frontier-observations.json',frontiers)
 q=normals[0,False]
 for label,path,value in [('subclassed nested error role',['output','last_pending_error_in_model','role'],S(q['output']['last_pending_error_in_model']['role'])),('subclassed output container',['output'],Dct(q['output']))]:
  bad=change(q,path,value);no(label,lambda bad=bad:m._construct_checked(b,bad),'CLEANUP-CONSTRUCTED-INPUT',where='exact-type input gate before predecessor construction validation')
 bad=D(q);v=bad['output'].pop('terminal_python_exception_in_model');bad['output'][S('terminal_python_exception_in_model')]=v
 no('subclassed literal flag key',lambda:m._construct_checked(b,bad),'CLEANUP-CONSTRUCTED-INPUT',where='exact-type input gate before predecessor construction validation')
 oldreceipt=(root/'results/recovered/cleanup-append.json').read_bytes();no('historical receipt stays historical and rejects corrected pins',lambda:m._receipt_checked(b,oldreceipt),'CLEANUP-STALE-OR-ALTERED-RECEIPT',where='authenticated-basis receipt-comparison core; no public negative derivation')
 public['contexts'].reverse();public['receipt']['sha256']='0'*64;public['actual_admission']=True
 yes('mutable public result cannot change current receipt expectation',lambda:m._receipt_checked(b,saved)['contexts']==list(m.CONTEXTS),'authenticated-basis receipt-comparison core')
 # Observe post-validation monitoring state; the unchanged LD01 tests are not rerun.
 sm=sys.monitoring;state={}
 for slot,p in ((3,b['prior_module']),(2,b['prior_basis']['prior_module'])):
  row={'owner':sm.get_tool(slot),'global':sm.get_events(slot),'local':sm.get_local_events(slot,p._basis.__code__)};cb=sm.register_callback(slot,sm.events.PY_RETURN,None)
  if cb is not None:sm.register_callback(slot,sm.events.PY_RETURN,cb)
  row['callback_present']=cb is not None;state[str(slot)]=row
  yes('normal authenticated completion monitoring state slot '+str(slot),lambda row=row:row=={'owner':None,'global':0,'local':0,'callback_present':False},'actual post-public normal monitoring-state inspection; no interruption campaign')
 r.save('normal-monitoring-state.json',state)
 r.save('validation-layers.json',{'full_current_public_positive':1,'actual_unchanged_predecessor_public_positive':1,'actual_returned_basis_used':True,'full_public_negative_derivations':0,'public_negative_calls':0,'focused_rows':layers,'constructed_cases_are_runtime_observations':False,'author_oracle_executed':False,'prepared_receipt_silently_repaired':False})
 r.save('closure-summary.json',{'EC01':'CLOSED within retained conditional correspondence contract','normal_retains_pending_original_and_true':True,'replacement_retains_true_with_correct_pending_error':True,'termination_unobserved_retain_none':True,'retained_witness_corrected_accepts_old_false_rejects':True,'both_contexts_and_control_prefixes':True,'no_residual_witness_found_in_bounded_checks':True,'runtime_observations_new':0,'line172_expanded':False,'prior_closures_reused':True,'admission':False})
