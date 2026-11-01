from pathlib import Path
import sys,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from lease_cases import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);stage=sys.argv[3];failure=None
try:
 r.save('input-verification.json',verify_root(root));guard(root,r.path,r);m=module(root/'code/correspondence.py');original=ValueError('LD01-SYNTHETIC-ORIGINAL');data,_,_,_=toy(m,root,'predecessor-failure',original)
 name={'local':'set_local_events','callback':'register_callback','release':'free_tool_id'}[stage]
 seen=interrupt(m,data,c_event='c_call',c_name=name,occurrence=2 if stage!='release' else 1,error=KeyboardInterrupt('LD01-CONSTRUCTED-CLEANUP-INTERRUPTION'))
 after=state(data);r.save('qualified-cleanup-state.json',{'injection':seen,'after':after,'candidate_cleanup_complete':False,'no_post_failure_reuse_demonstrated':True,'reviewer_lease_release':False,'callback_probe_restores_any_observed_callback':True,'termination_or_restart_not_candidate_cleanup':True})
 r.yes('cleanup interruption remains a distinct escaping error',lambda:'LD01-CONSTRUCTED-CLEANUP-INTERRUPTION' in seen['traceback'] and 'LD01-SYNTHETIC-ORIGINAL' in seen['traceback'])
 if stage=='local':r.yes('later unregister and release attempted; local events remain qualified',lambda:after['owner'] is None and after['callback_was_absent'] and after['local_events']==sys.monitoring.events.PY_RETURN)
 if stage=='callback':r.yes('later release attempted; callback remains qualified',lambda:after['owner'] is None and not after['callback_was_absent'] and after['local_events']==0)
 if stage=='release':r.yes('failed release retains owned marker; no successful reuse claim',lambda:after['owner'] is not None and after['callback_was_absent'] and after['local_events']==0)
 r.save('final-verification.json',verify_root(root))
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='Qualified synthetic cleanup-failure observation; not a candidate successful-release or reuse control',candidate_cleanup_complete=False,process_restart_not_candidate_release=True)
