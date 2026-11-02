"""One actual current public validation, then bounded independent checked-core review.
The new review checks are loaded only after authentication, with exact script identities saved.
No candidate function is replaced and no prepared basis substitutes for validation.
"""
from pathlib import Path
import sys,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
try:
 r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m);saved=(root/'results/recovered/cleanup-append.json').read_bytes()
 r.event('actual-public-validation-start',soft_deadline_seconds=3150,hard_timeout_seconds=3600,whole_chain_current_inputs=True)
 public=m.validate(root,saved);r.save('public-result.json',public)
 r.yes('actual current public accepts both contexts',lambda:public['result']=='PASS' and public['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and public['actual_admission'] is False)
 assert len(captures)==1;b=captures.pop();r.save('predecessor-public-result.json',b['public_predecessor']);r.save('catalogue.json',b['catalogue'])
 r.yes('actual unchanged LD01 predecessor public accepted',lambda:b['public_predecessor']['result']=='PASS' and b['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT)
 r.yes('actual authenticated current assembly equals saved receipt',lambda:m.enc(m._assemble(b['fresh'],m._rows(b),b))==saved)
 checks=Path(__file__).parent/'checks.py';helpers=[checks,Path(__file__).parent/'cases.py'];r.save('review-check-identities.json',{p.name:identity(p.read_bytes()) for p in helpers})
 r.event('focused-checks-start',uses_actual_authenticated_basis=True)
 check=module(checks);check.run(m,b,public,saved,r)
 r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='One actual current full public positive; actual unchanged predecessor; bounded authenticated-basis independent controls; recorded defects separate from successful controls',full_public_negative_derivations=0,CLI_execution_claimed=False)
