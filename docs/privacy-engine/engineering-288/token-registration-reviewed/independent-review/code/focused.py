from pathlib import Path
import sys,json,copy,traceback,ast,textwrap
sys.path.insert(0,str(Path(__file__).resolve().parent))
from common import *
from oracle import *
root=Path(sys.argv[1]).resolve();rec=Record(sys.argv[2]);error=None;cases=[]
class S(str):pass
class I(int):pass
class D(dict):pass
class L(list):pass
try:
 mon=guard(root);m=module(root/'code/correspondence.py');mon(m);data=m.inputs(root);cat=m.catalogue(data);rows,basis=m._checked(data,cat);c=data['coverage'];o=source_oracle(m.sources(data)[1]);rec.save('source-oracle.json',o)
 rec.check('actual predecessor derive_status invoked',lambda:sum(x['function']=='derive_status' for x in CALLS)==1)
 rec.check('catalogue exact stage coverage from independent AST',lambda:cat['source']['order']==o['order'] and [x['id'] for x in cat['declarations']]==o['order'] and set(cat['source']['stages'])==set(o['order']))
 for stage in o['order']:
  s=cat['source']['stages'][stage];rec.check('source site and source identity '+stage,lambda:s['site']==o['sites'][stage] and s['source']==o['entry'] and ast.dump(ast.parse(textwrap.dedent(' '*int(s['site'].split(':')[1])+s['expression'])))==ast.dump(ast.parse(o['expressions'][stage])))
 rec.check('control guard and failure guard are source conditions',lambda:cat['source']['control_guard']==o['control_guard'] and cat['source']['stored_failure_guard']==o['normal_guard'])
 rec.check('pop anchor is in actual finally region',lambda:any(g['kind']=='try' and g['region']=='finalbody' for g in cat['source']['stages']['removal-attempt']['guards']))
 for idx,row in enumerate(rows):
  tag=row['context'];normal,v,expect=make_case(row,o,c,cat,'review-selected-A',True,True);cases.append(normal)
  for name,opts in [('normal controlled',{}),('normal client only',{'control':False}),('normal unknown continuity',{'continuity':False}),('stored failure frontier',{'owner_none':False})]:
   case,va,ex=make_case(row,o,c,cat,'review-'+name,**opts);out=m._construct_checked(basis,case)['projection'];rec.check('source-derived '+name+' '+tag,lambda:out==case['output'])
  # Stopping outcomes preserve earlier facts but cannot create later milestones.
  for stage in ['registry-insert','control-callback','client-callback','finally-enter','removal-attempt','removal-complete']:
   for outcome in ['process-termination','unobserved','raise']:
    case,va,ex=make_case(row,o,c,cat,'review-stop-'+stage+'-'+outcome,stop=(stage,outcome));out=m._construct_checked(basis,case)['projection'];rec.check('prefix facts '+stage+' '+outcome+' '+tag,lambda:all(out[k]==val for k,val in ex.items()))
  for role in ['token','owner','client','control','session','manager','client.token','control.token','owners[token]','owner.wrapper','session.managed']:
   bad=copy.deepcopy(normal);bad['projection']['references'][role]['symbol']='wrong-role';rec.reject('wrong binding '+role+' '+tag,lambda:m._construct_checked(basis,bad),'TOKEN-REFERENCES')
  other,_,_=make_case(row,o,c,cat,'review-selected-B');bad=copy.deepcopy(normal);bad['projection']=copy.deepcopy(other['projection']);bad['output']=copy.deepcopy(other['output']);rec.reject('coordinated cross-invocation '+tag,lambda:m._construct_checked(basis,bad),'TOKEN-PREMISE')
  rec.check('equal phase content distinct invocation identities '+tag,lambda:normal['output']['events'][0]['id']!=other['output']['events'][0]['id'] and normal['output']['reference_bindings']['token']!=other['output']['reference_bindings']['token'])
  for field in ['acquisition','instance','frontier']:
   bad=copy.deepcopy(normal);bad['projection']['scope'][field]='stale';rec.reject('stale scope '+field+' '+tag,lambda:m._construct_checked(basis,bad),'TOKEN-PREMISE')
  for stage in ['registry-insert','control-guard','control-callback','owner-failure-guard','finally-enter','removal-attempt','removal-complete']:
   bad=copy.deepcopy(normal);before=len(bad['outcomes']);bad['outcomes']=[r for r in bad['outcomes'] if r['stage']!=stage];assert len(bad['outcomes'])==before-1;bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('actual omitted step '+stage+' '+tag,lambda:m._construct_checked(basis,bad))
  bad=copy.deepcopy(normal);bad['outcomes'][0],bad['outcomes'][2]=bad['outcomes'][2],bad['outcomes'][0];bad['projection']['outcomes']=copy.deepcopy(bad['outcomes']);rec.reject('insertion before owner rejected '+tag,lambda:m._construct_checked(basis,bad),'STEP-ORDER')
  for field in ['registration_completed_in_model','finally_entered_in_model','removal_attempt_entered_in_model','removal_completed_in_model','selected_owner_removed_in_model']:
   short,_,_=make_case(row,o,c,cat,'review-short',stop=('registry-insert','unobserved'));assert short['output'][field] is not True;short['output'][field]=True;rec.reject('no premature '+field+' '+tag,lambda:m._construct_checked(basis,short),'PROJECTION-CORRESPONDENCE')
  # An unobserved pop completion does not erase completed registration/finally/attempt.
  short,_,_=make_case(row,o,c,cat,'review-known-prefix',stop=('removal-complete','unobserved'))
  for field in ['registration_completed_in_model','client_callback_completed_in_model','finally_entered_in_model','removal_attempt_entered_in_model']:
   bad=copy.deepcopy(short);assert bad['output'][field] is True;bad['output'][field]=False;rec.reject('earlier established fact preserved '+field+' '+tag,lambda:m._construct_checked(basis,bad),'PROJECTION-CORRESPONDENCE')
  no,_,_=make_case(row,o,c,cat,'review-unknown-continuity',continuity=False);no['output']['selected_owner_removed_in_model']=True;rec.reject('continuity cannot be invented '+tag,lambda:m._construct_checked(basis,no),'PROJECTION-CORRESPONDENCE')
  for field,value in [('revocation_persists',True),('database_cleanup_completion',True),('retained_error',{}),('pop_return_value',normal['output']['reference_bindings']['owner']),('callback_return_destination','general client'),('actual_admission',True)]:
   bad=copy.deepcopy(normal);bad['output'][field]=value;rec.reject('unsupported '+field+' '+tag,lambda:m._construct_checked(basis,bad),'PROJECTION-CORRESPONDENCE')
  # Same-valued foreign types must be rejected before semantic rebuilding.
  for path,convert in [(('projection','occurrence'),S),(('projection','outcomes'),L),(('projection','scope'),D),(('output','completion'),S),(('output','events'),L),(('output','reference_bindings','token'),lambda z:{S(k):v for k,v in z.items()})]:
   bad=copy.deepcopy(normal);p=bad
   for k in path[:-1]:p=p[k]
   p[path[-1]]=convert(p[path[-1]]);assert enc(bad)==enc(normal);rec.reject('exact types '+str(path)+' '+tag,lambda:m._construct_checked(basis,bad))
  for field in ['control_present','owner_failure_none','registry_continuity']:
   bad=copy.deepcopy(normal);bad[field]=int(bad[field]);bad['projection'][field]=bad[field];rec.reject('exact boolean '+field+' '+tag,lambda:m._construct_checked(basis,bad),'TOKEN-BOOL')
  claimed=copy.deepcopy(rows);claimed[idx]['scope']['instance']=D(claimed[idx]['scope']['instance']);rec.reject('semantic nested subclass '+tag,lambda:m._check_rows(basis,claimed),'VALUE-TYPE')
  got=m._construct_checked(basis,normal);got['projection']['reference_bindings']['token']['scope']['instance'].clear();got['anchor'].clear();got['projection']['events'].reverse();rec.check('result aliases isolated '+tag,lambda:m._construct_checked(basis,normal)['projection']==normal['output'])
 # Coordinated generated coverage changes cannot set the source oracle.
 for name,edit in [('omit declaration and expected stage',lambda z:(z['declarations'].pop(),z['source']['order'].pop(),z['source']['stages'].pop('removal-complete'))),('replace pop key',lambda z:z['source']['remove'].update(key='other-token')),('erase optional control guard',lambda z:z['source'].update(control_guard='True')),('remove stored failure guard',lambda z:z['source'].update(stored_failure_guard='False')),('claim forwarded callback result',lambda z:z['source'].update(callback_returns_forwarded=True))]:
  bad=copy.deepcopy(cat);edit(bad);rec.reject('independent source validation '+name,lambda:c.validate_token_registration(*m.sources(data),*m.dependencies(data),m.inner(data)['ctx']['binding'],bad),'TOKEN-SOURCE-CORRESPONDENCE')
 bundle=m._assemble(data,rows,basis);raw=enc(bundle);rec.check('exact current receipt derived',lambda:raw==(root/'results/primary/token-registration-correspondence.json').read_bytes())
 bundle['contexts'].reverse();bundle['contexts'][0]['token_registration_correspondence']['declaration'].clear();rec.check('returned context mutations cannot change expected receipt',lambda:enc(m._assemble(data,rows,basis))==raw)
 rec.check('unchanged obligations and unavailable observations retained',lambda:json.loads(raw)['unchanged_obligations']=={'bytes':56813,'sha256':'2c92141711e260a2ef0271635562cbac5a71aae82ac7e1a52b5dbc6f228d3a45'} and all(r['runtime_registration_revocation_links'] is None and r['observer_join'] is None for r in rows))
 rec.save('independent-cases.json',{'cases':cases});rec.save('limits.json',json.loads(raw)['new_token_registration_limits'])
except BaseException:
 error=traceback.format_exc();(rec.path/'failure.txt').write_text(error);raise
finally:rec.finish(error,scope='Independent token normal-slice controls; source-derived conditional facts, no runtime execution')
