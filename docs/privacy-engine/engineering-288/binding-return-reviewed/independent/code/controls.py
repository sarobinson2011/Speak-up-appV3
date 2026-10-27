"""Independent bounded binding correspondence checks; saved inputs only."""
from pathlib import Path
import argparse,copy,hashlib,importlib.metadata,json,os,runpy,sys,traceback,types
def enc(v):return (json.dumps(v,sort_keys=True,separators=(',',':'),allow_nan=False)+'\n').encode()
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}
def module(p):
 m=types.ModuleType('independent_binding');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def main():
 p=argparse.ArgumentParser();p.add_argument('root',type=Path);p.add_argument('output',type=Path);p.add_argument('--recovered',action='store_true');a=p.parse_args();root=a.root.resolve();out=a.output.resolve();out.mkdir(parents=True,exist_ok=False)
 rows=[];error=None;constructed=[];calls=[];kinds={}
 def audit(event,args):
  if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
  if event=='exec' and args[0].co_filename.rsplit('/',1)[-1].lower() in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('PRODUCER-EXECUTION')
  if event=='open' and isinstance(args[0],(str,bytes)):
   name=os.fsdecode(args[0]);flags=args[2] or 0
   if name.startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
   if name.startswith(str(root)+'/') and flags&(os.O_WRONLY|os.O_RDWR|os.O_TRUNC|os.O_CREAT):raise AssertionError('INPUT-WRITE')
 sys.addaudithook(audit)
 def trace(frame,event,arg):
  if event!='call':return
  f=frame.f_code.co_filename;kind=kinds.get(f)
  if kind is None:
   n=f.rsplit('/',1)[-1].lower();kind=1 if n in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') else 2 if n=='prospective_entry.py' else 0;kinds[f]=kind
  name=frame.f_code.co_name
  if kind==1 or kind==2 and name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status'):raise AssertionError('APPLICATION-EXECUTION')
  parent=frame.f_back.f_code.co_name if frame.f_back else None
  if name=='derive_recovery' and parent=='_basis':calls.append({'function':'mandatory HF01 derive_recovery','file':f,'source':identity(Path(f).read_bytes())})
  if name=='_compare_evidence' and parent=='_checked':
   l=frame.f_locals;path='evidence/recovery-export-0.json';expected=json.loads(bytes.fromhex(json.loads(l['expected'][path])['head']))['binding'];candidate=l['candidate']
   value=None
   try:value=json.loads(bytes.fromhex(json.loads(candidate[path])['head'])).get('binding')
   except (ValueError,TypeError,KeyError):pass
   calls.append({'function':'binding comparison','expected':expected,'candidate':value})
 sys.settrace(trace)
 def record(label,category,result,**kw):
  r={'check':label,'category':category,'result':result,**kw};rows.append(r)
  with (out/'progress.jsonl').open('a') as f:f.write(json.dumps(r)+'\n')
 def check(label,fn,category='independent'):
  v=fn();assert v is not False,label;record(label,category,'PASS');return v
 def reject(label,fn,reason=None,category='negative'):
  try:fn()
  except (ValueError,TypeError,KeyError) as ex:
   if reason is not None:assert str(ex)==reason,(label,str(ex),reason)
   record(label,category,'REJECTED',error={'type':type(ex).__name__,'message':str(ex)});return
  raise AssertionError('UNEXPECTED-ACCEPTANCE:'+label)
 try:
  assert sys.version_info[:3]==(3,12,14) and not sys.flags.optimize
  m=module(root/'code/correspondence.py');data=m.inputs(root);cat=m.catalogue(data);d=data['prior_data'];e=dict(d['ctx']['e']);source={n:identity((root/'code'/n).read_bytes()) for n in ('correspondence.py','managed_coverage.py')}
  oracle=runpy.run_path(str(Path(__file__).with_name('source_oracle.py')))
  audit_result=check('independent defining-source types guards and return oracle',lambda:oracle['audit'](d['manager'],d['authority'],cat,d['values']['candidate/managed-route/model.json'],d['reference_module'].reference_catalogue(d),d['values']['candidate/managed-route/producers.json']['source_inventory']))
  (out/'source-audit.json').write_text(json.dumps(audit_result,indent=2)+'\n')
  claims=check('legitimate semantic correspondence',lambda:m.semantic(data,cat));bundle=check('legitimate derivation',lambda:m.derive_binding(data,cat));saved=(root/'results/binding-correspondence.json').read_bytes();check('derived receipt exact saved bytes',lambda:enc(bundle)==saved)
  public=check('legitimate public validation',lambda:m.validate(root,saved));old=json.loads((root/'retained/hf01/results/hf01-correspondence.json').read_bytes())
  export=json.loads(e['evidence/recovery-export-0.json']);state=json.loads(bytes.fromhex(export['head']));oldbinding=state['binding'];events=json.loads(e['evidence/execution-trace.json'])['events']
  check('no saved getter frame and no zero-count inference',lambda:all(t.get('function')!='ManagedAuthority.binding' for t in events) and bundle['new_binding_slice_limits']['actual_getter_count'] is None)
  cases=[]
  for i,row in enumerate(claims):
   name=row['context'];anchor=row['validated_binding_anchor'];prior=old['contexts'][i];new=bundle['contexts'][i]
   check('source catalogue independently matches '+name,lambda row=row:enc(row['declaration'])==enc(cat))
   check('all prior context members preserved '+name,lambda prior=prior,new=new:all(enc(new[k])==enc(v) for k,v in prior.items()))
   check('independent instance binding and exact HEAD bytes '+name,lambda anchor=anchor:anchor['binding_value']==state['binding']==anchor['instance']['binding'] and {k:anchor['record'][k] for k in ('bytes','sha256')}==identity(e['evidence/recovery-export-0.json']) and anchor['decoded_state']==identity(bytes.fromhex(export['head'])))
   check('predecessor acquisition occurrence and frame joins '+name,lambda anchor=anchor,prior=prior:anchor['record']==prior['hf01_evidence_binding']['head_record'] and anchor['instance']==prior['hf01_evidence_binding']['instance'] and anchor['recovery_occurrence']==prior['saved_recovery_fields'][0]['occurrence'] and anchor['recovery_frame']==prior['saved_recovery_fields'][0]['frame'] and anchor['recovery_parent']==prior['saved_recovery_fields'][0]['parent'] and anchor['record']['acquisition']==anchor['call']['acquisition'])
   check('reference value connection and missing-observation domains '+name,lambda row=row,anchor=anchor:row['getter_observations'] is None and all(anchor[k] is None for k in ('object_identity','underlying_connection_identity','getter_frame')))
   scope={'context':name,'acquisition':copy.deepcopy(anchor['record']['acquisition']),'recorded_instance':copy.deepcopy(anchor['instance']),'frontier':anchor['recovery_occurrence']};ref={'scope':scope,'symbol':'independent-reference-A'}
   case={'kind':'CONSTRUCTED-CONDITIONAL-GETTER','context':name,'anchor':copy.deepcopy(anchor),'premise':{'phase':'READY','live_reference':copy.deepcopy(ref),'retired_reference':None,'underlying':{'reference':copy.deepcopy(ref),'binding':oldbinding},'lock_enter_completed':True,'attribute_completed':True,'lock_exit_completed':True},'returned':oldbinding};cases.append(case)
   check('full conditional forwarding '+name,lambda case=case:m.constructed_projection(data,cat,case),'constructed_only');constructed.append(copy.deepcopy(case))
   other=copy.deepcopy(case);other['premise']['live_reference']['symbol']='independent-reference-B';other['premise']['underlying']['reference']['symbol']='independent-reference-B'
   projected=data['coverage'].binding_value_projection(cat,other['premise'],other['returned'])
   check('equal values retain distinct reference variables '+name,lambda projected=projected:projected['reference_symbol']['symbol']=='independent-reference-B','constructed_only')
   for label,edit in [('wrong receiver',lambda p:p['underlying']['reference'].update(symbol='wrong')),('not READY',lambda p:p.update(phase='CLOSED')),('missing live',lambda p:p.update(live_reference=None)),('retired present',lambda p:p.update(retired_reference=ref)),('lock entry not complete',lambda p:p.update(lock_enter_completed=False)),('attribute failure',lambda p:p.update(attribute_completed=False)),('lock exit failure',lambda p:p.update(lock_exit_completed=False)),('integer completion flag',lambda p:p.update(lock_exit_completed=1))]:
    if a.recovered and label not in ('wrong receiver','not READY'):continue
    premise=copy.deepcopy(case['premise']);edit(premise);reject('conditional guard '+label+' '+name,lambda premise=premise:data['coverage'].binding_value_projection(cat,premise,oldbinding),category='constructed_negative')
   for value in ([None,False,17,{},[]] if not a.recovered else [None,17]):reject('conditional return exact type '+name+' '+type(value).__name__,lambda value=value:data['coverage'].binding_value_projection(cat,case['premise'],value),'BINDING-VALUE-TYPE',category='constructed_negative')
   reject('conditional value origin '+name,lambda:data['coverage'].binding_value_projection(cat,case['premise'],'wrong'),'BINDING-VALUE-ORIGIN',category='constructed_negative')
  check('both exact ordered contexts',lambda:[x['context'] for x in claims]==['SYMBOLIC-U-ONE','SYMBOLIC-U-TWO'])
  badcase=copy.deepcopy(cases[0]);badcase['premise']['live_reference']['scope']['recorded_instance']['managed_constructor_frame']+=1;badcase['premise']['underlying']['reference']=copy.deepcopy(badcase['premise']['live_reference'])
  reject('full coordinated wrong-instance reference scope',lambda:m.constructed_projection(data,cat,badcase),'BINDING-CASE-REFERENCE-SCOPE')
  if not a.recovered:
   missingcase=copy.deepcopy(cases[1]);del missingcase['returned'];reject('full omitted getter value',lambda:m.constructed_projection(data,cat,missingcase),'BINDING-CASE-FIELDS')
   fakecase=copy.deepcopy(cases[0]);fakecase['kind']='OBSERVED-GETTER';reject('constructed result cannot become execution',lambda:m.constructed_projection(data,cat,fakecase),'BINDING-CASE-NOT-EXECUTION')
  for i in (0,1):
   bad=copy.deepcopy(claims);bad[i]['validated_binding_anchor']['instance']['managed_constructor_frame']+=1
   reject('semantic wrong instance with equal binding context '+str(i),lambda bad=bad:m.semantic(data,cat,bad),'BINDING-ANCHOR-LINEAGE')
   bad=copy.deepcopy(claims);bad[i]['validated_binding_anchor']['binding_value']=False
   reject('derivation wrong binding type context '+str(i),lambda bad=bad:m.derive_binding(data,cat,bad),'BINDING-ANCHOR-VALUE-TYPE')
   for label,edit in [('omitted value',lambda b:b.pop('binding_value')),('stale frontier',lambda b:b.update(recovery_occurrence='stale')),('cross acquisition',lambda b:b['record'].update(acquisition='foreign')),('invented getter frame',lambda b:b.update(getter_frame=123)),('coordinated value and instance',lambda b:(b.update(binding_value='f'*64),b['instance'].update(binding='f'*64)))]:
    if a.recovered and label not in ('omitted value','cross acquisition'):continue
    bad=copy.deepcopy(claims);edit(bad[i]['validated_binding_anchor']);reject('row relation '+label+' context '+str(i),lambda bad=bad:m._check_rows(bad,claims),category='internal_relation')
  # Independently substitute the binding wherever it occurs in saved JSON or
  # embedded JSON hex. The validator must use its reloaded predecessor value.
  newbinding=('f' if oldbinding[0]!='f' else 'e')+oldbinding[1:]
  def replace(v):
   if type(v) is str:
    if v==oldbinding:return newbinding
    try:raw=bytes.fromhex(v);nested=json.loads(raw)
    except (ValueError,UnicodeDecodeError):return v
    changed=replace(nested);return enc(changed).rstrip(b'\n').hex() if changed!=nested else v
   if type(v) is list:return [replace(x) for x in v]
   if type(v) is dict:return {k:replace(x) for k,x in v.items()}
   return v
  altered=dict(e);changes={}
  for n,b in e.items():
   if n.endswith('.json'):
    v=json.loads(b);changed=replace(v)
    if changed!=v:altered[n]=enc(changed);changes[n]={'before':identity(b),'after':identity(altered[n])}
  assert len(changes)>1 and json.loads(bytes.fromhex(json.loads(altered['evidence/recovery-export-0.json'])['head']))['binding']==newbinding
  (out/'coordinated-substitution.json').write_text(json.dumps({'old':oldbinding,'new':newbinding,'changed_members':changes,'source_and_database_bytes_unchanged':True},indent=2)+'\n')
  reject('coordinated reports semantic comparison',lambda:m.semantic(data,cat,evidence=altered),'BINDING-VALIDATED-INSTANCE-VALUE')
  reject('coordinated reports derivation comparison',lambda:m.derive_binding(data,cat,evidence=altered),'BINDING-VALIDATED-INSTANCE-VALUE')
  candidate=dict(data);candidate['prior_data']=dict(d);candidate['prior_data']['ctx']=dict(d['ctx']);candidate['prior_data']['ctx']['e']=altered
  if not a.recovered:reject('caller reports cannot replace expected binding',lambda:m.semantic(candidate,cat),'BINDING-VALIDATED-INSTANCE-VALUE')
  if not a.recovered:
   for label,edit in [('missing binding',lambda x:x.pop('binding')),('typed false binding',lambda x:x.update(binding=False)),('stale head same binding',lambda x:x.update(head='e'*64))]:
    value=copy.deepcopy(state);edit(value);ex=copy.deepcopy(export);ex['head']=enc(value).hex();ev=dict(e);ev['evidence/recovery-export-0.json']=enc(ex)
    reject('saved evidence '+label,lambda ev=ev:m._compare_evidence(e,ev,'binding'),category='internal_relation')
   ev=dict(e);del ev['evidence/client-handoff.json'];reject('full missing lineage member',lambda:m.semantic(data,cat,evidence=ev),'BINDING-EVIDENCE-MEMBERSHIP')
   badcat=copy.deepcopy(cat);badcat['source']['slot']='_retired';badcat['source']['value']['expression']='self._retired.binding';badcat['declaration']['origin']['expression']='self._retired.binding';badcat['reference_links']['live_read']['slot']='_retired'
   reject('coordinated catalogue source and reference substitution',lambda:m.derive_binding(data,badcat),'BINDING-SOURCE-CATALOGUE')
   for label,edit in [('lock guard',lambda c:c['source']['return'].update(guards=[])),('readiness guard',lambda c:c['source'].update(ready_phase='CLOSED')),('type',lambda c:c['declaration'].update(type='bool')),('return origin',lambda c:c['source'].pop('return'))]:
    c=copy.deepcopy(cat);edit(c);reject('producer rederives '+label,lambda c=c:data['coverage'].validate_binding_return(d['manager'],d['authority'],d['values']['candidate/managed-route/model.json'],d['values']['candidate/managed-route/producers.json'],d['guards']['guard_relationships'],d['guards']['guard_oracle'],d['reference_module'].reference_catalogue(d),c),'BINDING-RETURN-CORRESPONDENCE',category='source_negative')
  for i in (0,1):
   bad=copy.deepcopy(bundle);anchor=bad['contexts'][i]['binding_return_correspondence']['validated_binding_anchor'];anchor['binding_value']=newbinding;anchor['instance']['binding']=newbinding
   reject('public coordinated binding context '+str(i),lambda bad=bad:m.validate(root,enc(bad)),'STALE-OR-ALTERED-BINDING-CORRESPONDENCE',category='public_negative')
  if not a.recovered:
   for label,edit in [('omitted context',lambda b:b['contexts'].pop()),('duplicated context',lambda b:b['contexts'].__setitem__(1,copy.deepcopy(b['contexts'][0]))),('runtime and admission escalation',lambda b:b['new_binding_slice_limits'].update(actual_getter_count=0,saved_getter_execution_evidence='COMPLETE',actual_admission=True))]:
    bad=copy.deepcopy(bundle);edit(bad);reject('public '+label,lambda bad=bad:m.validate(root,enc(bad)),'STALE-OR-ALTERED-BINDING-CORRESPONDENCE',category='public_negative')
  exactclaims=enc(claims);othercontext=enc(claims[1]);claims[0]['validated_binding_anchor']['instance'].clear();claims[0]['declaration']['source']['ready_phase']='CLOSED'
  check('nested context trees do not alias',lambda:enc(claims[1])==othercontext)
  public['contexts'].reverse();public['receipt'].clear();bundle['contexts'].reverse();bundle['contexts'][0]['binding_return_correspondence']['validated_binding_anchor'].clear()
  originalcat=enc(cat);cat['declaration']['inherited_binding']['native_template']['type']='BOOLEAN'
  check('returned catalogue cannot change expectation',lambda:enc(m.catalogue(data))==originalcat)
  cat=m.catalogue(data);check('pristine semantic unchanged after nested mutations',lambda:enc(m.semantic(data,cat))==exactclaims)
  check('pristine derivation unchanged after nested mutations',lambda:enc(m.derive_binding(data,cat))==saved)
  check('pristine public survives nested mutations',lambda:m.validate(root,saved))
  check('mandatory predecessor actually invoked',lambda:any(x['function']=='mandatory HF01 derive_recovery' for x in calls))
  check('comparison used validated original binding',lambda:any(x['function']=='binding comparison' and x['candidate']==newbinding and x['expected']==oldbinding for x in calls))
  check('implementation and candidate evidence unchanged',lambda:source=={n:identity((root/'code'/n).read_bytes()) for n in source} and e==d['ctx']['e'])
 except BaseException as ex:error={'type':type(ex).__name__,'message':str(ex)};(out/'failure.txt').write_text(traceback.format_exc());raise
 finally:
  sys.settrace(None);r={'result':'PASS' if error is None else 'FAIL','assertions':len(rows),'categories':{c:sum(x['category']==c for x in rows) for c in sorted({x['category'] for x in rows})},'checks':rows,'error':error,'recovered':a.recovered,'environment':{'python':sys.version,'optimization':sys.flags.optimize,'cryptography_installed':importlib.metadata.version('cryptography')},'source':locals().get('source'),'database_connections':0,'session_operations':0,'completed_review_reruns':False,'constructed_cases_are_execution_evidence':False}
  (out/'RESULT.json').write_text(json.dumps(r,indent=2)+'\n');(out/'call-observations.json').write_text(json.dumps(calls,indent=2)+'\n');(out/'constructed-cases.json').write_text(json.dumps(constructed,indent=2)+'\n')
 print('PASS',len(rows),'independent binding checks')
if __name__=='__main__':main()
