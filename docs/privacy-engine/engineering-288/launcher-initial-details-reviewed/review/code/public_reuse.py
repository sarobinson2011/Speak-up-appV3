"""One new actual recovered-root public validation after two candidate-cleaned interruptions."""
from pathlib import Path
import sys,json,traceback,copy
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from lease_probe import *
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
try:
 r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m);data=m.inputs(root);saved=(root/'ld01/receipts/corrected-launcher-details.json').read_bytes();before=identity(saved)
 r.event('interruption-checks-start',same_process_public_reuse_follows=True)
 for mode in ('source-boundary','c-return'):
  result=interrupt(m,data,mode);after=state(data['prior_module']);result['after']=after;r.save(mode+'.json',result)
  r.yes(mode+' reached successfully reserved live invocation marker',lambda:result['observation']['owner_is_marker'] and result['observation']['marker_present'])
  r.yes(mode+' before callback bookkeeping',lambda:not result['observation']['capture_defined'])
  r.yes(mode+' candidate clears reservation event mask and callback',lambda:clean(after))
 r.event('actual-public-validation-start',prior_interruption_count=2,reviewer_release=False,restart=False,root=str(root))
 public=m.validate(root,saved);r.save('public-result.json',public)
 r.yes('same-process actual public validation accepts both contexts',lambda:public['result']=='PASS' and public['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and public['actual_admission'] is False)
 assert len(captures)==1;b=captures.pop();r.save('predecessor-public-result.json',b['public_predecessor'])
 r.yes('actual unchanged predecessor public validation authenticated',lambda:b['public_predecessor']['result']=='PASS' and b['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT)
 after=state(b['prior_module']);r.save('after-validation.json',after)
 r.yes('normal actual validation cleans all checked monitoring state',lambda:clean(after))
 r.yes('actual authenticated reassembly equals corrected saved receipt',lambda:m.enc(m._assemble(b['fresh'],m._rows(b),b))==saved)
 old=(root/'results/primary/launcher-details.json').read_bytes()
 r.no('old pin receipt rejects at authenticated receipt-comparison core',lambda:m._receipt_checked(b,old),'DETAILS-STALE-OR-ALTERED-RECEIPT')
 altered=json.loads(saved);altered['extension_components']['correspondence.py']['sha256']='0'*64;raw=m.enc(altered)
 r.no('substituted component rejects at authenticated receipt-comparison core',lambda:m._receipt_checked(b,raw),'DETAILS-STALE-OR-ALTERED-RECEIPT')
 r.yes('submitted receipt bytes and saved input remain unrepaired',lambda:identity(saved)==before and raw==m.enc(altered) and (root/'results/primary/launcher-details.json').read_bytes()==old)
 public['contexts'].reverse();public['receipt'].clear()
 r.yes('mutable returned public result cannot alter comparison expectations',lambda:m._receipt_checked(b,saved)['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
 r.yes('prior context mappings and boundaries unchanged',lambda:json.loads(saved)['contexts']==json.loads(old)['contexts'])
 r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='One actual same-process current public positive after source-boundary and C-return interruptions; unchanged predecessor; receipt-comparison negatives separately identified',full_public_negative_derivations=0,reviewer_release_between_interruption_and_validation=False)
