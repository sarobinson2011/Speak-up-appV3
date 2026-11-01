from pathlib import Path
import sys,traceback,json,copy
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from lease_cases import *
root=Path(sys.argv[1]);r=Records(sys.argv[2]);mode=sys.argv[3];failure=None
try:
 r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root);points=boundaries(m);saved=(root/'ld01/receipts/corrected-launcher-details.json').read_bytes()
 # An actual public rejection at the contention gate, before predecessor work.
 sm=sys.monitoring;foreign='LD01-public-contention-fixture';sm.use_tool_id(2,foreign)
 try:r.no('actual public contention gate remains fail-closed',lambda:m.validate(root,saved),'DETAILS-MONITORING-CONTENTION');r.yes('public contention preserves foreign lease',lambda:sm.get_tool(2) is foreign)
 finally:
  if sm.get_tool(2) is foreign:sm.free_tool_id(2)
 # No reviewer release or restart between this injection and actual validation.
 kw={'line':points['capture']} if mode=='primary' else {'c_event':'c_return','c_name':'use_tool_id'}
 seen=interrupt(m,data,**kw);after=state(data);r.save('corrected-interruption.json',{'injection':seen,'after':after,'reviewer_release':False,'candidate_functions_replaced':False,'same_process_reuse_follows':True})
 r.yes('source-derived post-reservation interruption reached owned slot',lambda:seen['owner_is_invocation_marker'] is True)
 r.yes('candidate released owned lease callbacks and events before reuse',lambda:clean(after))
 r.event('actual_public_reuse_begin',same_process=True,reviewer_release_since_interruption=False)
 public=m.validate(root,saved);r.save('actual-public-result.json',public)
 r.yes('actual pristine public validation succeeds after corrected interruption',lambda:public['result']=='PASS' and public['contexts']==list(m.CONTEXTS))
 assert len(captures)==1;basis=captures[0]
 r.save('actual-predecessor-public-result.json',basis['public_predecessor']);r.yes('actual unchanged predecessor public validation succeeds',lambda:basis['public_predecessor']['result']=='PASS' and basis['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT)
 r.yes('actual current reassembly exactly matches prepared receipt',lambda:m.enc(m._assemble(basis['fresh'],m._rows(basis),basis))==saved)
 actual_after=state({'prior_module':basis['prior_module']});r.save('after-actual-validation.json',actual_after);r.yes('candidate released resources after actual public completion',lambda:clean(actual_after))
 old=(root/'results/primary/launcher-details.json').read_bytes();before=json.loads(old);now=json.loads(saved)
 r.yes('both contexts and both-prefix source declarations unchanged',lambda:before['contexts']==now['contexts'])
 r.yes('only declared correspondence component pin changed in receipt',lambda:{k:v for k,v in before.items() if k!='extension_components'}=={k:v for k,v in now.items() if k!='extension_components'} and before['extension_components']['managed_coverage.py']==now['extension_components']['managed_coverage.py'])
 r.no('old component receipt rejects at authenticated comparison core only',lambda:m._receipt_checked(basis,old),'DETAILS-STALE-OR-ALTERED-RECEIPT')
 public['contexts'].clear();r.yes('returned result mutation cannot change authenticated expectations',lambda:m._receipt_checked(basis,saved)['contexts']==list(m.CONTEXTS))
 r.save('final-verification.json',verify_root(root))
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='LD01 actual same-process pristine public reuse after candidate cleanup; unchanged predecessor validator; saved inputs only',mode=mode,prior_campaigns_replayed=False,full_public_negative_derivations_claimed=0,negative_layers=['actual public monitoring-contention gate','authenticated receipt-comparison core'],runtime_observations_available=False)
