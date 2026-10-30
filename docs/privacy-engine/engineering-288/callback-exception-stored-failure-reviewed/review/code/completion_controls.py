from pathlib import Path
import sys,traceback,json
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import ORDER,independently_check
root=Path(sys.argv[1]).resolve();fixturepath=Path(sys.argv[2]).resolve();rec=Records(sys.argv[3]);err=None
try:
 rec.save('input-verification.json',verify_root(root));guard(root,rec.path);c=module(root/'code/managed_coverage.py');receipt=json.loads((root/'results/primary/callback-stored-failure.json').read_bytes());cases=json.loads(fixturepath.read_bytes());rec.save('review-fixture-identity.json',{'identity':ident(fixturepath.read_bytes()),'origin':'Fresh primary review fixtures; independent mandatory adapter validation, not supplied control results'})
 for base in cases:
  idx=0 if base['context']=='SYMBOLIC-U-ONE' else 1;cat=receipt['contexts'][idx]['callback_stored_failure_correspondence']['declaration'];label=base['context']+'/'+base['failure_route']
  variants=[('callback-handler-enter','process-termination','callback_handler_entry_completed_in_model',True),('callback-failure-guard','raise','established_explicit_cause',base['output']['established_explicit_cause']),('finally-enter','unobserved','finally_entry_completed_in_model',True),('removal-attempt','raise','removal_completed_in_model',True),('removal-complete','unobserved','removal_completed_in_model',True),('removal-complete','raise','established_explicit_cause',None)]
  for stage,terminal,field,val in variants:
   x=D(base);i=ORDER.index(stage);path=ORDER[:i+1]+ORDER[3:] if terminal=='raise' and i<3 else ORDER[:i+1]
   outcomes=[{'stage':s,'outcome':terminal if s==stage else 'raised-stored-from-client' if s==ORDER[2] else 'normal'} for s in path];x['outcomes']=outcomes;x['projection']['outcomes']=D(outcomes);v=D(x['projection']);x['output']=c.callback_failure_projection(cat,x['projection'],v)
   assert independently_check(x);wrong=change(x['output'],(field,),D(val));rec.no('false completion/prior-fact erasure '+label+'/'+stage+'/'+terminal+'/'+field,lambda wrong=wrong,x=x,v=v:c.validate_callback_failure_projection(cat,x['projection'],v,wrong))
 rec.save('final-verification.json',verify_root(root))
except BaseException:
 err=traceback.format_exc();(rec.path/'failure.txt').write_text(err);raise
finally:rec.finish(err,scope='Pure output-validation negatives using freshly independently validated finite fixtures; no standalone runtime/binding claim')
