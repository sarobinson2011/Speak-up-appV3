"""One actual recovered public validation, then focused EC-01 closure controls.
No candidate replacement, supplied-campaign replay or prepared authentication.
"""
from pathlib import Path
import sys,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
try:
 r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m);saved=(root/'ec01/receipts/prepared-cleanup-append.json').read_bytes()
 r.save('submitted-receipt-identity.json',identity(saved));r.event('actual-current-public-start',soft_control_deadline_seconds=3150,hard_timeout_seconds=3600)
 public=m.validate(root,saved);r.save('actual-public-result.json',public)
 r.yes('actual corrected public positive both contexts',lambda:public['result']=='PASS' and public['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and public['receipt']==identity(saved) and public['actual_admission'] is False)
 assert len(captures)==1;b=captures.pop();r.save('unchanged-predecessor-public-result.json',b['public_predecessor'])
 r.yes('actual unchanged predecessor public positive',lambda:b['public_predecessor']['result']=='PASS' and b['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT)
 r.yes('authenticated current assembly matches exact new receipt',lambda:m.enc(m._assemble(b['fresh'],m._rows(b),b))==saved)
 checks=Path(__file__).parent/'checks.py';r.save('review-check-identities.json',{p.name:identity(p.read_bytes()) for p in [checks,*[Path(__file__).parent/n for n in ('cases.py','parent_cases.py','parent_details.py','common.py')]]})
 r.event('focused-closure-start',actual_returned_basis=True);module(checks).run(m,b,public,saved,r)
 r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='EC01 only: one fresh recovered public positive and focused actual-authenticated-basis controls; no earlier review or campaign replay',full_public_negative_derivations=0,public_negative_calls=0,CLI_execution_claimed=False)
