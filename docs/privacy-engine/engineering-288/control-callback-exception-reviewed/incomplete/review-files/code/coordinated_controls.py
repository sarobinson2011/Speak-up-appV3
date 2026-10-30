from pathlib import Path
import sys,json
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import PREFIX,ORDER
root=Path(sys.argv[1]);fixtures=Path(sys.argv[2]);r=Records(sys.argv[3]);error=None
try:
 guard(root,r.path);c=module(root/'code/managed_coverage.py');saved=json.loads((root/'results/primary/control-exception.json').read_bytes());cases=json.loads(fixtures.read_bytes());r.save('independently_authenticated_fixture_identity.json',ident(fixtures.read_bytes()))
 for idx,x in enumerate(cases):
  cat=saved['contexts'][idx]['control_exception_revocation_correspondence']['declaration'];base=x['projection']
  def reject(label,q):
   assert enc(q)!=enc(base),'NO-OP-MUTATION:'+label
   before=enc(q);r.no(label,lambda:c.control_exception_projection(cat,q,D(q)));assert enc(q)==before,'INPUT-REPAIR:'+label
  for j in range(len(PREFIX)):
   q=D(base);q['token_inputs']['outcomes'].pop(j);reject('coordinated prefix omission '+str((idx,j)),q)
   q=D(base);q['token_inputs']['outcomes'].insert(j,D(q['token_inputs']['outcomes'][j]));reject('coordinated prefix duplicate '+str((idx,j)),q)
  for j in range(len(PREFIX)-1):
   q=D(base);a=q['token_inputs']['outcomes'];a[j],a[j+1]=a[j+1],a[j];reject('coordinated prefix reorder '+str((idx,j)),q)
  for k in ('registration_completed_in_model','control_callback_completed_in_model','client_callback_completed_in_model','finally_entered_in_model','removal_completed_in_model'):
   q=D(base);q['token_prefix'][k]=not q['token_prefix'][k];reject('mutually altered token prefix must be recomputed '+str((idx,k)),q)
  for k in ('process-termination','unobserved','normal'):
   q=D(base);q['token_inputs']['outcomes'][-1]['outcome']=k;reject('wrong control frontier '+str((idx,k)),q)
  for field in ('owner_failure_none','control_present','registry_continuity'):
   for value in (0,1):
    q=D(base);q['token_inputs'][field]=value;reject('prefix exact bool '+str((idx,field,value)),q)
  for name in ('owner','token','control'):
   q=replace(base,base['references'][name]['symbol'],'foreign/'+name);reject('all paired reference copies substituted '+str((idx,name)),q)
  for key,value in [('reference','wrong/error'),('callback_occurrence','wrong/callback'),('callee','client'),('existing_cause',None),('existing_context',None),('existing_suppression',False),('local_handler_binding','client_error')]:
   q=D(base);q['control_error'][key]=value;reject('both error reports substituted '+str((idx,key)),q)
  for k in ('raise','process-termination','unobserved'):
   q=D(base);q['outcomes']=[{'stage':'finally-enter','outcome':k},{'stage':'removal-attempt','outcome':'normal'}];reject('invented continuation after stopped frontier '+str((idx,k)),q)
  for s in ('client-create','client-callback','callback-handler-enter','owner-failure-guard'):
   q=D(base);q['outcomes'].insert(0,{'stage':s,'outcome':'normal'});reject('invented client or stored-error step '+str((idx,s)),q)
  q=D(base);snapshot=enc(q);out=c.control_exception_projection(cat,q,q);out['control_error']['scope'].clear();out['events'].clear()
  r.yes('legitimate shared input aliases and returned isolation '+str(idx),lambda:enc(q)==snapshot and c.control_exception_projection(cat,q,q)==x['output'])
  q=D(base);q['control_error']['cycle']=q;r.no('coordinated cyclic input '+str(idx),lambda:c.control_exception_projection(cat,q,q))
  for key in ('owner_failure_guard_evaluated_in_model','client_handler_entered_in_model','new_explicit_cause_assignment_established_in_model'):
   bad=change(x['output'],(key,),True);r.no('direct submitted-output coordinated claim '+str((idx,key)),lambda bad=bad:c.validate_control_exception_projection(cat,base,D(base),bad))
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:r.finish(error,scope='Paired in-memory substitutions over newly independently authenticated fixtures; not standalone evidence authentication')
