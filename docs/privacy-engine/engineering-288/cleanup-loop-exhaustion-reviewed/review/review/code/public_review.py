"""One actual fresh recovered public positive followed by focused independent checks."""
from pathlib import Path
import sys,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
root=Path(sys.argv[1]).resolve();r=Records(sys.argv[2]);failure=None
try:
 r.save('input-verification.json',verify_root(root));monitor,captures=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m)
 saved=(root/'receipts/prepared-cleanup-loop.json').read_bytes();r.save('submitted-receipt-identity.json',identity(saved));r.event('actual-public-start',hard_timeout=5000,control_deadline=4400)
 public=m.validate(root,saved);r.save('actual-public-result.json',public)
 r.yes('actual current public positive both contexts',lambda:public['result']=='PASS' and public['contexts']==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'] and public['receipt']==identity(saved) and public['actual_admission'] is False,'full current public validation on recovered root')
 assert len(captures)==1;b=captures.pop();r.save('actual-predecessor-public-result.json',b['public_predecessor'])
 r.yes('actual unchanged line172 predecessor public positive',lambda:b['public_predecessor']['result']=='PASS' and b['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT,'actual unchanged predecessor public validation')
 r.yes('exact prepared receipt equals actual authenticated assembly',lambda:m.enc(m._assemble(b['fresh'],m._rows(b),b))==saved,'authenticated-basis receipt assembly')
 r.save('executed-review-code-identities.json',{p.name:identity(p.read_bytes()) for p in Path(__file__).parent.glob('*.py')})
 r.event('focused-independent-start',actual_authenticated_basis=True);module(Path(__file__).parent/'checks.py').run(m,b,public,saved,r)
 r.save('final-verification.json',verify_root(root));r.event('finished')
except BaseException:
 failure=traceback.format_exc();(r.path/'failure.txt').write_text(failure);raise
finally:r.finish(failure,scope='Only bounded cleanup-loop exhaustion correspondence; prior reviews reused',full_public_negative_derivations=0)
