"""Only the unrecovered public coordinated receipt check; all confirmed rows reused."""
from pathlib import Path
import sys,json,traceback
root=Path(sys.argv[1]).absolute();sys.path.insert(0,str(root/'tests'))
from offline import *
rec=Record(sys.argv[2]);error=None
try:
 rec.save('input-verification.json',verify_root(root));monitor=guard(root,rec.path);m=module(root/'code/correspondence.py');monitor(m)
 raw=(root/'results/primary/control-construction.json').read_bytes();q=json.loads(raw)
 for ctx in q['contexts']:
  r=ctx['control_construction_revocation_correspondence'];r['declaration']['source']['completed_control_object_established']=True;r['construction_completed']=True;r['control_callback_execution']=True
 altered=m.enc(q);(rec.path/'coordinated-claims-receipt.json').write_bytes(altered)
 rec.save('witness.json',{'original':identity(raw),'submitted':identity(altered),'contexts':[c['context'] for c in q['contexts']],'changes_per_context':['declaration.source.completed_control_object_established: false -> true','construction_completed: false -> true','control_callback_execution: false -> true'],'actual_validator_input_saved':True,'other_input_or_code_changes':False})
 print('Only unfinished both-context coordinated public receipt comparison; one invocation',flush=True)
 try:m.validate(root,altered)
 except ValueError as ex:
  assert str(ex)=='CONSTRUCTION-STALE-OR-ALTERED-RECEIPT',(type(ex).__name__,str(ex))
  (rec.path/'validator-rejection.traceback.txt').write_text(traceback.format_exc())
  rec.save('validator-rejection.json',{'type':type(ex).__name__,'error':str(ex),'layer':'Public post-derivation receipt comparison in correspondence.validate','other_layer_result_inferred':False,'validator_invocations':1})
  rec.row('public coordinated completed construction and callback claim','REJECTED',error=str(ex))
 else:raise AssertionError('UNEXPECTED-ACCEPTANCE')
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='One unfinished public check only; original 285 and 71 corroborated rows remain separately interrupted evidence',validator_invocations=1)
