from pathlib import Path
import sys,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import ORDER
root=Path(sys.argv[1]).resolve();fixture_path=Path(sys.argv[2]);rec=Records(sys.argv[3]);err=None
try:
 guard(root,rec.path);c=module(root/'code/managed_coverage.py');saved=json.loads((root/'results/primary/callback-bare-rethrow.json').read_bytes());fixtures=json.loads(fixture_path.read_bytes())
 for idx,x in enumerate(fixtures):
  cat=saved['contexts'][idx]['callback_bare_rethrow_correspondence']['declaration'];p=x['projection']
  def reject(label,q):
   assert enc(q)!=enc(p),'No-op mutation: '+label
   rec.no(label,lambda:c.callback_bare_projection(cat,q,D(q)))
  for j in range(6):
   q=D(p);del q['outcomes'][j];reject('coordinated omitted stage '+str((idx,j)),q)
   q=D(p);q['outcomes'].insert(j,D(q['outcomes'][j]));reject('coordinated duplicate stage '+str((idx,j)),q)
  for j in range(5):
   q=D(p);q['outcomes'][j],q['outcomes'][j+1]=q['outcomes'][j+1],q['outcomes'][j];reject('coordinated reordering '+str((idx,j)),q)
  for value in [0,False,'None',[],{}]:reject('coordinated invalid None slot '+str((idx,type(value).__name__)),change(p,('none_guard_binding','slot_value'),value))
  reject('coordinated false guard truth '+str(idx),change(p,('none_guard_binding','guard_result'),True))
  for stage in ORDER:
   q=D(p);q['outcomes'][ORDER.index(stage)]['outcome']='normal-return';reject('unsupported stage outcome '+str((idx,stage)),q)
  for completion,outcome in [('process-termination','process-termination'),('unobserved-continuation','unobserved'),('normal-pop-completion','normal')]:
   q=D(p);q['token_prefix']['completion']=completion;q['token_prefix']['events'][-1]['outcome']=outcome;reject('coordinated unsupported callback prefix '+str((idx,completion)),q)
  # Shared input aliases with ordinary exact values remain source-admitted.
  q=D(p);q['none_guard_binding']['scope']=q['scope'];q['callback_error']['scope']=q['scope']
  out=c.callback_bare_projection(cat,q,D(q));rec.yes('shared input values accepted '+str(idx),lambda:out==x['output'])
  out['callback_error']['scope']['instance'].clear();rec.yes('returned alias cannot edit input '+str(idx),lambda:bool(q['scope']['instance']))
  before=dict(q['none_guard_binding']);q['none_guard_binding']['loop']=q['none_guard_binding'];rec.no('cyclic exact tree rejects before normalization '+str(idx),lambda:c.callback_bare_projection(cat,q,q))
  rec.no('invented existing chain absence output '+str(idx),lambda:c.validate_callback_bare_projection(cat,p,D(p),change(x['output'],('exception_chain_observation','existing_cause'),None)))
 rec.save('fixture-identity.json',ident(fixture_path.read_bytes()))
except BaseException:
 err=traceback.format_exc();(rec.path/'failure.txt').write_text(err);raise
finally:rec.finish(err,scope='Additional coordinated pure producer controls over freshly independently validated fixtures; not independent evidence authentication')
