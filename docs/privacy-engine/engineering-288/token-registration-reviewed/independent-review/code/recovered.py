from pathlib import Path
import sys,json,copy,traceback
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from oracle import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None
class S(str):pass
class I(int):pass
class D(dict):pass
try:
 mon=guard(root);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);c=data['coverage'];o=source_oracle(m.sources(data)[1]);raw=(root/'results/primary/token-registration-correspondence.json').read_bytes()
 rec.check('recovered actual predecessor and exact current receipt',lambda:sum(x['function']=='derive_status' for x in CALLS)==1 and enc(m._assemble(data,rows,basis))==raw)
 for idx,row in enumerate(rows):
  tag=row['context']
  for name,opts,expected in [('plain no-control',{'control':False},'normal-pop-completion'),('unknown continuity',{'continuity':False},'normal-pop-completion'),('stored failure',{'owner_none':False},'stored-failure-exceptional-frontier'),('finally unknown',{'stop':('finally-enter','unobserved')},'unobserved-continuation'),('pop raises',{'stop':('removal-complete','raise')},'unexpected-raise'),('pop terminates',{'stop':('removal-complete','process-termination')},'process-termination')]:
   fx,v,known=make_case(row,o,c,cat,'recovered-'+name,**opts);got=m._construct_checked(basis,fx)['projection'];rec.check('source completion '+name+' '+tag,lambda:got['completion']==expected and all(got[k]==x for k,x in known.items()))
  normal,v,_=make_case(row,o,c,cat,'recovered-A')
  # Once a normal pop is explicitly established in the model, unknown outer cleanup does not erase it.
  rec.check('normal pop and known earlier facts coexist with outer gaps '+tag,lambda:normal['output']['registration_completed_in_model'] and normal['output']['removal_completed_in_model'] and normal['output']['database_cleanup_completion'] is None and normal['output']['revocation_persists'] is None)
  for field in ['token','owner','client.token','control.token','owner.wrapper','session.managed']:
   bad=copy.deepcopy(normal);bad['projection']['references'][field]['scope']['invocation']='other-invocation';rec.reject('recovered nested scope '+field+' '+tag,lambda:m._construct_checked(basis,bad),'TOKEN-REFERENCES')
  bad=copy.deepcopy(normal);bad['projection']['scope']['context']=rows[1-idx]['context'];rec.reject('cross-context scope '+tag,lambda:m._construct_checked(basis,bad),'TOKEN-PREMISE')
  early,_,_=make_case(row,o,c,cat,'recovered-partial',stop=('removal-attempt','unobserved'));early['output']['removal_completed_in_model']=True;rec.reject('attempt absence cannot establish completion '+tag,lambda:m._construct_checked(basis,early),'PROJECTION-CORRESPONDENCE')
  for field,conv in [('completion',S),('events',tuple),('reference_bindings',D)]:
   bad=copy.deepcopy(normal['output']);bad[field]=conv(bad[field]);assert enc(bad)==enc(normal['output']);rec.reject('submitted output exact type '+field+' '+tag,lambda:c.validate_token_registration_projection(cat,normal['projection'],v,bad))
  bad=copy.deepcopy(normal['projection']);bad['references']['token']={S(k):x for k,x in bad['references']['token'].items()};rec.reject('producer nested key exact type '+tag,lambda:c.token_registration_projection(cat,bad,v),'KEY-TYPE')
  claims=copy.deepcopy(rows);claims[idx]['declaration']['source']['entry']['bytes']=I(claims[idx]['declaration']['source']['entry']['bytes']);rec.reject('semantic nested scalar preflight '+tag,lambda:m.semantic(data,cat,claims),'VALUE-TYPE')
  out=m._construct_checked(basis,normal);out['anchor'].clear();out['projection']['events'].clear();rec.check('recovered return alias isolation '+tag,lambda:m._construct_checked(basis,normal)['projection']==normal['output'])
 # Isolate mandatory source/claims and evidence validation from saved-result summaries.
 for label,change in [('missing context',lambda v:v.pop()),('duplicate context',lambda v:v.__setitem__(1,copy.deepcopy(v[0]))),('reversed contexts',lambda v:v.reverse()),('omitted conditional link',lambda v:v[0]['conditional_links'].pop()),('runtime evidence invented',lambda v:v[1].update(runtime_registration_revocation_links=[]))]:
  claims=copy.deepcopy(rows);change(claims);rec.reject('required claims '+label,lambda:m._check_rows(basis,claims))
 for label,change in [('missing trace',lambda v:v.pop('evidence/execution-trace.json')),('changed trace',lambda v:v.__setitem__('evidence/execution-trace.json',v['evidence/execution-trace.json']+b' '))]:
  ev=dict(basis['evidence']);change(ev);rec.reject('fresh validated evidence '+label,lambda:m._compare_evidence(basis,ev),'TOKEN-VALIDATED-EVIDENCE')
 rec.check('all retained limits exact in both contexts',lambda:all(r['classification']=='UNKNOWN' and r['multiplicity'] is None and r['ordinal'] is None and r['observer_join'] is None for r in rows))
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Independent distinct recovered-root controls; no runtime registration/removal observation')
