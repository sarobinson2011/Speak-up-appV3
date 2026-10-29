"""Distinct recovery controls; exact recovered root before consuming code."""
from pathlib import Path
import sys,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from offline import *
from cases import *
root=Path(sys.argv[1]).absolute();rec=Record(sys.argv[2]);error=None
class S(str):pass
class D(dict):pass
class L(list):pass
try:
 rec.save('input-verification.json',verify_root(root));mon=guard(root,rec.path);m=module(root/'code/correspondence.py');mon(m);d=m.inputs(root);cat=m.catalogue(d);rows,basis=m._checked(d,cat);c=d['coverage'];saved=(root/'results/primary/token-registration-correspondence.json').read_bytes()
 rec.check('recovered actual mandatory predecessor invoked',lambda:sum(x['function']=='derive_status' for x in CALLS)==1)
 rec.check('recovered exact saved receipt reproduction',lambda:m.enc(m._assemble(d,rows,basis))==saved)
 for idx in (0,1):
  tag=rows[idx]['context'];fx=normal(m,basis,idx)
  for label,case in [('controlled normal',fx),('client-only normal',normal(m,basis,idx,control=False)),('unknown continuity normal pop',normal(m,basis,idx,continuity=False)),('stored failure frontier',normal(m,basis,idx,owner_none=False))]:rec.check(label+' '+tag,lambda case=case:m._construct_checked(basis,case)['projection']==case['output'])
  for stage in ('registry-insert','client-callback','finally-enter','removal-attempt','removal-complete'):
   case=normal(m,basis,idx,terminal=(stage,'process-termination'));out=m._construct_checked(basis,case)['projection'];rec.check(stage+' termination no unwind/removal proof '+tag,lambda out=out:out['outcome_classification']['terminal_python_exception_in_model'] is None and out['retained_error'] is None and out['database_cleanup_completion'] is None and not out['removal_completed_in_model'])
  bad=normal(m,basis,idx,terminal=('removal-complete','unobserved'));bad['output']['removal_completed_in_model']=True;rec.reject('unobserved pop cannot confirm completion '+tag,lambda:m._construct_checked(basis,bad))
  bad=copy.deepcopy(fx);bad['projection']['references']['token']['symbol']='stale';rec.reject('wrong token '+tag,lambda:m._construct_checked(basis,bad))
  bad=copy.deepcopy(fx);bad['projection']['references']['owners[token]']['symbol']='stale';rec.reject('wrong selected owner '+tag,lambda:m._construct_checked(basis,bad))
  other=normal(m,basis,idx,invocation='foreign');bad=copy.deepcopy(fx);bad['projection']=other['projection'];bad['output']=other['output'];rec.reject('coordinated cross-invocation '+tag,lambda:m._construct_checked(basis,bad))
  bad=copy.deepcopy(fx);bad['outcomes'].pop(2);bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('missing registry insertion '+tag,lambda:m._construct_checked(basis,bad))
  bad=copy.deepcopy(fx);bad['output']['events'].reverse();rec.reject('reordered returned events '+tag,lambda:m._construct_checked(basis,bad))
  bad=copy.deepcopy(fx);bad['output']['reference_bindings']['token']={S(k):v for k,v in bad['output']['reference_bindings']['token'].items()};rec.reject('exact nested literal key '+tag,lambda:m._construct_checked(basis,bad))
  bad=copy.deepcopy(fx);bad['projection']['outcomes']=L(bad['projection']['outcomes']);rec.reject('exact input list '+tag,lambda:m._construct_checked(basis,bad))
  bad=copy.deepcopy(fx);bad['output']['completion']=S(bad['output']['completion']);rec.reject('exact output string '+tag,lambda:m._construct_checked(basis,bad))
  bad=copy.deepcopy(rows);bad[idx]['scope']['instance']=D(bad[idx]['scope']['instance']);rec.reject('exact nested semantic claim '+tag,lambda:m._check_rows(basis,bad))
  claims=copy.deepcopy(rows);claims[idx]['declaration']['source']['remove']['key']='foreign';rec.reject('coordinated source/claim cannot change expectation '+tag,lambda:m._check_rows(basis,claims))
  got=m._construct_checked(basis,fx);got['anchor'].clear();got['projection']['events'].clear();rec.check('returned nested mutation isolated '+tag,lambda:m._construct_checked(basis,fx)['projection']==fx['output'])
 # Adjacent evidence controls use actual predecessor evidence, not reports.
 expected=basis['evidence'];key='evidence/execution-trace.json'
 bad=copy.deepcopy(expected);v=json.loads(bad[key]);v['events'][0]['seq']=999;bad[key]=m.enc(v);rec.reject('altered saved trace rejects against validated predecessor',lambda:m._compare_evidence(basis,bad))
 bad=copy.deepcopy(expected);bad.pop(key);rec.reject('missing saved binding evidence rejects',lambda:m._compare_evidence(basis,bad))
 bad={S(k):v for k,v in expected.items()};rec.reject('evidence key subclasses reject before equality',lambda:m._compare_evidence(basis,bad))
 bad=copy.deepcopy(cat);bad['declarations'].pop();rec.reject('recovered source coverage omission',lambda:c.validate_token_registration(*m.sources(d),*m.dependencies(d),m.inner(d)['ctx']['binding'],bad))
 rec.check('all prior UNKNOWN totals and boundary flags retained',lambda:m._assemble(d,rows,basis)['new_token_registration_limits']['inventory_unknown_totals']==4 and m._assemble(d,rows,basis)['new_token_registration_limits']['lifetime_unknown_totals']==14 and not m._assemble(d,rows,basis)['actual_admission'] if 'actual_admission' in m._assemble(d,rows,basis) else m._assemble(d,rows,basis)['new_token_registration_limits']['actual_admission'] is False)
 rec.check('observer remains unjoined, no actual registration or removal observations',lambda:all(r['observer_join'] is None and r['runtime_registration_revocation_links'] is None for r in rows))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Engineering distinct recovered-root controls only; prior results not merged')
