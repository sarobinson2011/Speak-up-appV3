"""Isolated qualified residual-state observations; no cleanup or reuse success claim."""
from pathlib import Path
import sys,ast,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from synthetic import *
from lease_probe import state
root=Path(sys.argv[1]);r=Records(sys.argv[2]);kind=sys.argv[3];failure=None;sm=sys.monitoring;profile=sys.getprofile()
try:
 r.save('input-verification.json',verify_root(root));guard(root,r.path,r);m=module(root/'code/correspondence.py');tree=ast.parse((root/'code/correspondence.py').read_bytes());f=next(n for n in tree.body if isinstance(n,ast.FunctionDef) and n.name=='_public_predecessor');outer=next(n for n in f.body if isinstance(n,ast.Try));first=outer.finalbody[0].body[0];second=first.finalbody[0];lines={'local':first.body[0].lineno,'callback':second.body[0].lineno,'release':second.finalbody[0].lineno};names={'local':'set_local_events','callback':'register_callback','release':'free_tool_id'}
 original=ValueError('FL6-original-predecessor-error');one=KeyboardInterrupt('FL6-first-cleanup-interruption');two=KeyboardInterrupt('FL6-second-cleanup-interruption');data,counts=fixture(m,'before',error=original);seen=[];selected='local' if kind=='repeated' else kind;caught=None
 def interrupt_cleanup(frame,event,arg):
  if frame.f_code is m._public_predecessor.__code__ and frame.f_lineno==lines[selected] and event=='c_call' and arg is getattr(sm,names[selected]) and not seen:
   seen.append({'step':selected,'hook':'profile c_call','line':frame.f_lineno,'offset':frame.f_lasti});raise one
 def second_interrupt(event,args):
  if kind=='repeated' and event=='sys.monitoring.register_callback':
   frame=sys._getframe(1)
   if frame.f_code is m._public_predecessor.__code__ and frame.f_lineno==lines['callback']:
    seen.append({'step':'callback','hook':'audit before callback unregister','line':frame.f_lineno,'offset':frame.f_lasti});raise two
 sys.addaudithook(second_interrupt)
 try:
  sys.setprofile(interrupt_cleanup)
  try:m._public_predecessor(data)
  except BaseException as e:caught=e;tb=traceback.format_exc()
 finally:sys.setprofile(profile)
 assert caught is (two if kind=='repeated' else one),repr(caught)
 chain=[];current=caught
 while current is not None and len(chain)<8:chain.append({'type':type(current).__name__,'message':str(current)});current=current.__context__
 assert any(x['message']==str(original) for x in chain),chain
 after=state(data['prior_module'])
 expected={'local':(True,sm.events.PY_RETURN,False),'callback':(True,0,True),'release':(False,0,False),'repeated':(True,sm.events.PY_RETURN,True)}[kind]
 assert (after['owner'] is None,after['local_events'],after['callback_present'])==expected,(kind,after)
 assert after['global_events']==0 and len(seen)==(2 if kind=='repeated' else 1)
 r.row('cleanup exception supersedes pending predecessor error; original retained in constructed chain','QUALIFIED-OBSERVATION',kind=kind)
 r.row('residual monitoring state preserved without reviewer release or successful reuse claim','QUALIFIED-OBSERVATION',kind=kind)
 r.save('qualified-state.json',{'kind':kind,'injections':seen,'exception_chain':chain,'after':after,'candidate_cleanup_complete':False,'post_failure_reuse_tested':False,'reviewer_release':False,'free_slot_not_proof_of_complete_cleanup':True,'process_exit_not_candidate_cleanup':True});(r.path/'traceback.txt').write_text(tb);r.save('final-verification.json',verify_root(root))
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:
 sys.setprofile(profile);r.finish(failure,scope='Qualified real-monitoring cleanup-failure observations with synthetic predecessor; outside successful cleanup/reuse claims',candidate_cleanup_complete=False,process_termination_or_exit_not_cleanup_evidence=True)
