import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from cases import normal,refresh,independently_check,ORDER
import argparse
def run(root,out,mode):
 r=Records(out);monitor=guard(root,out)
 try:
  r.save('input-verification.json',verify_root(root));m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root);cat=m.catalogue(data)
  rows,b=m._checked(data,cat);r.yes('fresh mandatory source/evidence validation',lambda:len(rows)==2)
  receipt=m._assemble(data,rows,b);saved=(root/'results/primary/callback-bare-rethrow.json').read_bytes();r.yes('derived current receipt equals exact saved bytes',lambda:enc(receipt)==saved);r.save('receipt-identity.json',ident(saved))
  for i,row in enumerate(receipt['contexts']):
   for key in ('stored_failure_revocation_correspondence','callback_stored_failure_correspondence'):
    r.yes('prior relation exact '+str(i)+' '+key,lambda i=i,key=key:row[key]==b['prior']['contexts'][i][key])
  fixtures=[]
  for idx in (0,1):
   x=normal(m,b,idx);fixtures.append(x);c=b['fresh']['coverage']
   def good(label,q):
    r.yes(label,lambda:m._construct_checked(b,q)['projection']==q['output'] and independently_check(q))
   def bad(label,q):r.no(label,lambda:m._construct_checked(b,q))
   good('normal bare path '+str(idx),x)
   for control,cont in [(False,True),(True,False)]:good('optional control/continuity '+str((idx,control,cont)),normal(m,b,idx,control=control,continuity=cont))
   alt=normal(m,b,idx,inv='FL6-bare-distinct-'+str(idx));good('distinct constructed invocation '+str(idx),alt)
   r.yes('equal kind does not merge occurrence '+str(idx),lambda:x['output']['events'][0]['id']!=alt['output']['events'][0]['id'])
   stages=ORDER if mode=='primary' else [ORDER[1],ORDER[2],ORDER[4]]
   for stage in stages:
    for outcome in ('raise','process-termination','unobserved'):
     q=normal(m,b,idx,terminal=(stage,outcome));good('frontier '+str((idx,stage,outcome)),q)
     # Output mutations cannot erase acknowledged facts or create completion.
     field='bare_rethrow_completed_in_model' if stage in ORDER[:3] else 'removal_completed_in_model'
     bad('false completion '+str((idx,stage,outcome)),change(q,('output',field),True))
   for key,value in [('existing_cause',None),('existing_context',None),('existing_suppression',False),('physical_reference_observation','object-address')]:bad('invented chain '+str((idx,key)),change(x,('output','exception_chain_observation',key),value))
   bad('invented explicit cause '+str(idx),change(x,('output','new_explicit_cause_assignment_established_in_model'),True))
   for path,value in [(('none_guard_binding','slot_value'),False),(('none_guard_binding','guard_result'),0),(('none_guard_binding','slot_exact_type'),'bool'),(('none_guard_binding','slot'),'other.failure'),(('callback_error','reference'),'wrong/error'),(('callback_error','scope','invocation'),'wrong'),(('context',),'SYMBOLIC-U-TWO' if idx==0 else 'SYMBOLIC-U-ONE'),(('anchor','context'),'wrong'),(('token_case','owner_failure_none'),False)]:bad('wrong selected binding '+str((idx,path)),change(x,path,value))
   for j in (range(6) if mode=='primary' else [1,4]):
    q=D(x);del q['outcomes'][j];bad('missing stage '+str((idx,j)),q)
    q=D(x);q['outcomes'].insert(j,D(q['outcomes'][j]));bad('duplicate stage '+str((idx,j)),q)
   for j in (range(5) if mode=='primary' else [1]):
    q=D(x);q['outcomes'][j],q['outcomes'][j+1]=q['outcomes'][j+1],q['outcomes'][j];bad('reordered stage '+str((idx,j)),q)
   # Coordinated substitutions across all trace/projection/result duplicates.
   for label,old,new in [('error',x['callback_error']['reference'],'foreign/error'),('owner',x['projection']['references']['owner']['symbol'],'foreign/owner'),('token',x['projection']['references']['token']['symbol'],'foreign/token'),('acquisition',x['projection']['scope']['acquisition'],'foreign-acquisition')]:bad('coordinated '+label+' '+str(idx),replace(x,old,new))
   q=D(x);q['none_guard_binding']['slot_value']=0;q['projection']['none_guard_binding']['slot_value']=0;q['output']['none_guard_binding']['slot_value']=0;bad('coordinated non-None slot '+str(idx),q)
   q=D(x);q['token_case']['output']['registration_completed_in_model']=False;q['projection']['token_prefix']['registration_completed_in_model']=False;q['output']['validated_token_prefix']['registration_completed_in_model']=False;bad('coordinated no registration '+str(idx),q)
   for field in ('runtime_observation','callback_reaches_launcher_established','run_success_established','actual_admission','obligations_discharged'):bad('unsupported status '+str((idx,field)),change(x,('output',field),True))
   class S(str):pass
   class I(int):pass
   class L(list):pass
   class M(dict):pass
   for path,value in [(('callback_error','role'),S(x['callback_error']['role'])),(('outcomes',),L(x['outcomes'])),(('none_guard_binding',),M(x['none_guard_binding'])),(('output','callback_raised_in_model'),I(1)),(('output','bare_raise_semantics','adds_explicit_cause'),0)]:bad('exact nested types '+str((idx,path)),change(x,path,value))
   q=D(x);v=q['none_guard_binding'].pop('slot_value');q['none_guard_binding'][S('slot_value')]=v;bad('subclassed literal key '+str(idx),q)
   returned=m._construct_checked(b,x);returned['projection']['events'].reverse();returned['projection']['callback_error']['scope']['instance'].clear()
   good('returned nested mutation isolates expectations '+str(idx),x)
   # Producer output boundary under the independently authenticated premises.
   v=m._premises(b,x);r.no('producer submitted-output false normal '+str(idx),lambda:c.validate_callback_bare_projection(cat,x['projection'],v,change(x['output'],('completion',),'normal-return')))
  r.save('fixtures.json',fixtures)
  # Source/semantic claims do not acquire runtime observations through a copy.
  returned=m._rows(b);returned.reverse();returned[0]['declaration']['source']['order'].reverse()
  r.no('semantic returned context/order mutation rejected',lambda:m._check_rows(b,returned))
  r.yes('fresh rows retain declared contexts',lambda:[q['context'] for q in m._rows(b)]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  r.no('missing semantic context',lambda:m._check_rows(b,rows[:1]))
  r.no('duplicate semantic context',lambda:m._check_rows(b,[rows[0],rows[0]]))
  r.no('semantic observation escalation',lambda:m._check_rows(b,change(rows,(0,'runtime_callback_bare_revocation_chain'),[])))
  if mode=='primary':
   # One fresh semantic call after returned-object mutation; underlying saved
   # evidence is checked again, not expectations recycled from the mutated result.
   after=m.semantic(data,cat);r.yes('fresh semantic after nested mutation stays pristine',lambda:after==rows)
   evidence=D(m.inner(data)['ctx']['e']);key=next(k for k,v in evidence.items() if v);evidence[key]=evidence[key]+b'\n'
   r.no('fresh semantic altered authenticated evidence',lambda:m.semantic(data,cat,evidence=evidence),'EVIDENCE')
  r.save('final-verification.json',verify_root(root));r.finish()
 except BaseException:
  error=traceback.format_exc();r.save('failure.txt',error);r.finish(error);raise
if __name__=='__main__':
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--mode',choices=['primary','recovered'],required=True);a=p.parse_args();run(a.root,a.output,a.mode)
