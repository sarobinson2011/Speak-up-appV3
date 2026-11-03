"""One actual public positive; then focused cores using its actual returned basis."""
from pathlib import Path
import sys,signal,json,traceback
sys.path.insert(0,str(Path(__file__).parent))
from common import *
from independent_model import source_plan,check_source,oracle,build
root=Path(sys.argv[1]);fixture_root=Path(sys.argv[2]);r=Records(sys.argv[3]);error=None
def alarm(*args):raise TimeoutError('REVIEW-SOFT-TIMEOUT; unfinished checks are not passes')
signal.signal(signal.SIGALRM,alarm);signal.alarm(4500)
class Text(str):pass
class Items(list):pass
class Number(int):pass
def main():
 r.save('input-root.json',verify_root(root));r.save('environment.json',environment());monitor,captures=guard(root,r.path,r);m=module(root/'code/correspondence.py');monitor(m)
 # Real C-return interruption immediately after successful slot1 acquisition.
 # No predecessor call occurs in this mechanism fixture; actual validation follows
 # in this same process, with no reviewer release or restart.
 class Interrupted(RuntimeError):pass
 def dummy_basis(data):return None
 p=types.SimpleNamespace(_basis=dummy_basis);hit=[];sm=sys.monitoring
 def profile(frame,event,arg):
  if frame.f_code is m._public_predecessor.__code__ and event=='c_return' and arg is sm.use_tool_id:
   sys.setprofile(None);hit.append(True);raise Interrupted('after successful C-level acquisition')
 def release_trial():
  sys.setprofile(profile)
  try:
   try:m._public_predecessor({'prior_module':p})
   except Interrupted:pass
   else:raise AssertionError('intended acquisition interruption not delivered')
  finally:sys.setprofile(None)
  assert hit==[True] and sm.get_tool(1) is None and sm.get_local_events(1,dummy_basis.__code__)==0
  return True
 r.yes('slot1 C-return interruption released by candidate before actual public reuse',release_trial,'real monitoring mechanism with synthetic predecessor; not authentication')
 raw=(root/'receipts/prepared-write-call-replacement.json').read_bytes();r.save('receipt-identity.json',identity(raw));r.event('actual-public-started',receipt=identity(raw))
 result=r.yes('fresh recovered actual public validation',lambda:m.validate(root,raw),'FULL PUBLIC POSITIVE through unchanged actual predecessor')
 r.save('actual-public-result.json',result);assert len(captures)==1;b=captures[0];c=b['fresh']['coverage'];cat=b['catalogue'];rows=m._rows(b)
 r.yes('returned basis is from exactly one actual public chain',lambda:len(captures)==1 and b['public_predecessor']['result']=='PASS' and b['public_predecessor']['receipt']==m.PREDECESSOR_RECEIPT,'actual public return observation')
 r.save('predecessor-public-result.json',b['public_predecessor']);r.save('basis-facts.json',{'catalogue':identity(m.enc(cat)),'source_identities':[identity(x) for x in b['fresh']['sources']],'evidence':{k:identity(v) for k,v in b['evidence'].items()},'session_bindings':b['session_bindings']})
 plan=source_plan((root/'source-evidence/lab_bootstrap.py').read_bytes());r.yes('complete source regions, dependency edges and exact positions',lambda:check_source(cat,plan),'independent source AST compared with authenticated catalogue')
 r.yes('both symbolic contexts required in declared order',lambda:tuple(x['context'] for x in rows)==m.CONTEXTS,'authenticated-basis semantic core')
 r.yes('actual assembled receipt exact saved bytes',lambda:m.enc(m._assemble(b['fresh'],rows,b))==raw,'authenticated-basis receipt comparison core')
 def slots_free():return all(sys.monitoring.get_tool(i) is None and sys.monitoring.get_events(i)==0 for i in range(1,6))
 r.yes('observer reservation/global masks released after actual public',slots_free,'monitoring state observation; not proof of every local callback cleanup')
 r.save('monitoring-state.json',{'slots':{i:{'owner':sys.monitoring.get_tool(i),'global':sys.monitoring.get_events(i)} for i in range(1,6)},'local_and_callback_complete_cleanup':'not inferred from free slots'})
 public_layer='public entry pre-derivation shape gate'
 receipt=json.loads(raw)
 for label,v in [('missing relation',change(receipt,('contexts',0),{k:v for k,v in receipt['contexts'][0].items() if k!=m.RELATION})),('one context',change(receipt,('contexts',),receipt['contexts'][:1])),('wrong format',change(receipt,('format',),'old'))]:
  r.no(label,lambda v=v:m.validate(root,m.enc(v)),'WC-MANDATORY-RELATIONS',public_layer)
 layer='authenticated-basis receipt comparison core; not full public negative derivation'
 for label,v in [('reversed contexts',change(receipt,('contexts',),list(reversed(receipt['contexts'])))),('invented admission',change(receipt,('new_write_call_limits','actual_admission'),True)),('invented observed invocation',change(receipt,('contexts',0,m.RELATION,'actual_invocation_count'),1)),('substituted context',change(receipt,('contexts',1,'context'),m.CONTEXTS[0]))]:
  r.no(label,lambda v=v:m._receipt_checked(b,m.enc(v)),'WC-STALE-OR-ALTERED-RECEIPT',layer)
 r.no('whitespace substitution rejected without repair',lambda:m._receipt_checked(b,enc(receipt)),'WC-STALE-OR-ALTERED-RECEIPT',layer)
 def receipt_isolation():
  made=m._assemble(b['fresh'],rows,b);made['contexts'][0][m.RELATION]['session_binding']['instance'].clear();made['contexts'].reverse();result['contexts'].reverse();return m.enc(m._assemble(b['fresh'],m._rows(b),b))==raw and m._receipt_checked(b,raw)['contexts']==list(m.CONTEXTS)
 r.yes('returned public result and nested receipt do not mutate expectations',receipt_isolation,'authenticated-basis repeated comparison core')
 semantic_layer='authenticated-basis candidate/semantic comparison core'
 for label,claimed in [('reversed semantic rows',list(reversed(rows))),('nested wrong destination',change(rows,(0,'session_binding','recorded_destination'),'/invented')),('false runtime observation',change(rows,(1,'write_call_attempt_observed'),True)),('literal key subclass',{Text('x'):1})]:
  r.no(label,lambda claimed=claimed:m._check_candidate(b,b['fresh'],cat,claimed,b['evidence']),'WC-',semantic_layer)
 def rows_isolation():
  a=m._rows(b);a[0]['declaration']['source']['steps'][0]['inputs'].append('invented');a[1]['session_binding']['instance'].clear();return m._check_candidate(b,b['fresh'],cat,m._rows(b),b['evidence'])==rows
 r.yes('nested returned rows isolated',rows_isolation,semantic_layer)
 for label,key,value in [('stale predecessor bytes','prior_saved',b['fresh']['prior_saved']+b' '),('substituted source','sources',(b['fresh']['sources'][0]+b'\n',*b['fresh']['sources'][1:]))]:
  data=dict(b['fresh']);data[key]=value;r.no(label,lambda data=data:m._check_candidate(b,data,cat),'WC-CANDIDATE-',semantic_layer)
 altered=dict(b['evidence']);k=next(k for k in altered if k.endswith('SMOKE-ABOUT-TO-START.json'));altered[k]=altered[k]+b' '
 r.no('stale exact destination evidence',lambda:m._check_candidate(b,b['fresh'],cat,rows,altered),'WC-VALIDATED-EVIDENCE',semantic_layer)
 # Coordinated catalogue and semantic-row mutations still compare against actual basis.
 mutated=D(cat);mutated['source']['steps'][1]['name']='not_write_new';claims=D(rows)
 for row in claims:row['declaration']=D(mutated)
 r.no('coordinated catalogue/claims substitution',lambda:m._check_candidate(b,b['fresh'],mutated,claims),'WC-CATALOGUE-SOURCE',semantic_layer)
 steps=cat['source']['steps'];core='authenticated-parent producer projection/output comparison core'
 for ix,path in enumerate(sorted(fixture_root.glob('*.json'))):
  case=json.loads(path.read_bytes());label=path.stem;r.event('case-started',case=label)
  v=r.yes(label+' revalidates selected actual predecessor case',lambda case=case:m._premises(b,case),'authenticated-basis mandatory predecessor constructed-case validation')
  actual=c.write_call_projection(cat,case['projection'],v)
  r.yes(label+' independent normal semantics, values, references and limits',lambda:oracle(cat,case,actual),core)
  r.yes(label+' prepared output equals actual authenticated-parent derivation',lambda:c.validate_write_call_projection(cat,case['projection'],v,case['output']),core)
  if ix in (0,4):r.yes(label+' full constructed entry from actual basis',lambda:m._construct_checked(b,case)['projection']==actual,'authenticated-basis mandatory constructed-case core')
  r.save('normal-'+label+'.json',actual)
  # Each context/prefix/origin receives a different early/late frontier, four outcomes.
  selected=[0,1,8,12,20,28,len(steps)-2,len(steps)-1][ix];selected=min(selected,len(steps)-1)
  for outcome in ('raise','catchable-interruption','process-termination','unobserved'):
   mutant=build(c,cat,case['parent_case'],case['session_binding'],(steps[selected]['id'],outcome));vv=D(v);vv['outcomes']=D(mutant['outcomes'])
   out=c.write_call_projection(cat,mutant['projection'],vv)
   r.yes(label+' '+str(selected)+' '+outcome+' first frontier semantics',lambda:oracle(cat,mutant,out),core)
   wrong=change(out,('terminal_python_exception_in_model',),False)
   r.no(label+' '+outcome+' cannot erase pending/uncertain exception',lambda:c.validate_write_call_projection(cat,mutant['projection'],vv,wrong),'WC-OUTPUT-CORRESPONDENCE',core)
   too_far=D(mutant['projection']);too_far['outcomes'].append({'stage':'after-first-frontier','outcome':'normal'});tv=D(vv);tv['outcomes']=D(too_far['outcomes'])
   r.no(label+' '+outcome+' cannot continue after first frontier',lambda:c.write_call_projection(cat,too_far,tv),'WC-UNREACHED-STEPS',core)
  # All normal outputs must retain exact source constants and established parent facts.
  for key,value in [('terminal_python_exception_in_model',1),('write_new_body_entry_established',True),('normal_overall_return_established',True),('pid_value',0),('cleanup_list_state',{}),('original_error_pending_in_outer_handler',None),('call_arguments',{'p':None,'x':None})]:
   bad=change(actual,(key,),value);r.no(label+' reject '+key,lambda bad=bad:c.validate_write_call_projection(cat,case['projection'],v,bad),'WC-OUTPUT-CORRESPONDENCE',core)
  bad=change(actual,('events',0,'stage'),Text(actual['events'][0]['stage']));r.no(label+' reject same-valued str subclass',lambda:c.validate_write_call_projection(cat,case['projection'],v,bad),'WC-OUTPUT-TYPE',core)
  # Input order/omission and a coordinated owner substitution do not bypass trusted premises.
  for desc,oo in [('omission',case['outcomes'][1:]),('reorder',[case['outcomes'][1],case['outcomes'][0],*case['outcomes'][2:]])]:
   cv=D(case['projection']);cv['outcomes']=oo;vv=D(v);vv['outcomes']=D(oo);r.no(label+' '+desc,lambda cv=cv,vv=vv:c.write_call_projection(cat,cv,vv),'WC-ORDER',core)
  cv=D(case['projection']);cv['binding']['references']['owner']={'invented':'owner'};r.no(label+' coordinated changed owner rejected against authenticated expectation',lambda:c.write_call_projection(cat,cv,v),'WC-VALIDATED:binding',core)
  def isolated():
   out=c.write_call_projection(cat,case['projection'],v);out['binding']['references'].clear();out['values'].clear();out['cleanup_list_state'].clear();return c.write_call_projection(cat,case['projection'],v)==actual
  r.yes(label+' nested output mutation isolation',isolated,core)
  if ix in (0,4):
   u=build(c,cat,case['parent_case'],case['session_binding'],(steps[0]['id'],'unobserved'),'UNESTABLISHED');uv=D(v);uv['binding']=D(u['binding']);uv['outcomes']=D(u['outcomes']);uo=c.write_call_projection(cat,u['projection'],uv)
   r.yes(label+' unestablished continuity retains uncertainty and no evaluation',lambda:oracle(cat,u,uo),core)
   uv['outcomes']=D(case['outcomes']);cv=D(u['projection']);cv['outcomes']=D(case['outcomes']);r.no(label+' unestablished continuity cannot admit normal sequence',lambda:c.write_call_projection(cat,cv,uv),'WC-UNKNOWN-CONTINUITY',core)
   for desc,wrongcase in [('wrong invocation',change(case,('invocation',),'foreign-invocation')),('wrong session',change(case,('session_binding','recorded_destination'),'/foreign')),('invented parent completion',change(case,('parent_output','loop_completion_established'),False))]:
    r.no(label+' '+desc,lambda wrongcase=wrongcase:m._construct_checked(b,wrongcase),'WC-', 'authenticated-basis mandatory constructed-case core')
   old=case['parent_output']['original_error_pending_in_outer_handler'];new=D(old);assert type(new) is dict;new['role']='invented-original-error';assert new!=old
   coordinated=D(case);coordinated['parent_output']['original_error_pending_in_outer_handler']=new;coordinated['binding']['original_constructor_error']=D(new);coordinated['projection']['parent_result']=D(coordinated['parent_output']);coordinated['projection']['binding']=D(coordinated['binding'])
   r.no(label+' coordinated original-error substitution',lambda:m._construct_checked(b,coordinated),'WC-VALIDATED-PARENT','authenticated-basis mandatory constructed-case core')
 r.save('final-root.json',verify_root(root));r.save('limits.json',{'authentic_public_positives':1,'full_public_negative_derivations':0,'constructed_cases_are_runtime':False,'retained_slots_2_3_4_5_campaigns_replayed':False,'runtime_frames_PID_path_filename_unobserved':True,'host_50_0_2_not_qualified':True})
 r.event('finished',checks=len(r.rows))
try:main()
except BaseException:
 error=traceback.format_exc();(r.path/'failure.txt').write_text(error);raise
finally:
 signal.alarm(0);r.finish(error,scope='NEW line174 bounded independent review; supplied and historical campaigns not replayed')
