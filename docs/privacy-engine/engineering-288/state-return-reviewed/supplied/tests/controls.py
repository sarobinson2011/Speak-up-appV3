"""Focused new state controls; no completed suite or runtime entry invoked."""
import argparse,ast,copy,hashlib,json,os,sys,time,types
from pathlib import Path
def audit(event,args):
 if event.startswith('sqlite3.connect') or event in ('socket.connect','socket.bind','socket.getaddrinfo','subprocess.Popen','os.system','os.fork','os.posix_spawn'):raise AssertionError('PROHIBITED:'+event)
 if event=='open' and isinstance(args[0],(str,bytes)) and os.fsdecode(args[0]).startswith('/home/steve/'):raise AssertionError('HOST-ACCESS')
 if event=='exec' and args[0].co_filename.rsplit('/',1)[-1] in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py'):raise AssertionError('APPLICATION-EXECUTION')
sys.addaudithook(audit)
_file_kind={}
def guard(frame,event,arg):
 if event!='call':return None
 filename=frame.f_code.co_filename;kind=_file_kind.get(filename)
 if kind is None:
  name=filename.rsplit('/',1)[-1];kind=1 if name in ('authority.py','live_connection.py','lab_bootstrap.py','worker.py') else 2 if name=='prospective_entry.py' else 0;_file_kind[filename]=kind
 if kind==1 or kind==2 and frame.f_code.co_name in ('main','run','run_controlled','_run','_dispatch','__init__','state','handle','status'):raise AssertionError('APPLICATION-EXECUTION')
 return None
sys.settrace(guard)
def module(p):
 m=types.ModuleType('_state_controls');m.__file__=str(p);exec(compile(p.read_bytes(),str(p),'exec'),m.__dict__);return m
def identity(b):return {'bytes':len(b),'sha256':hashlib.sha256(b).hexdigest()}

def main():
 p=argparse.ArgumentParser();p.add_argument('--root',type=Path,required=True);p.add_argument('--output',type=Path,required=True);p.add_argument('--write',action='store_true');p.add_argument('--recovered',action='store_true');a=p.parse_args();a.output.mkdir(parents=True,exist_ok=False)
 rows=[];cases=[];paths=[];error=None;start=time.monotonic()
 def check(label,fn):
  v=fn();assert v is not False,label;row={'check':label,'result':'PASS'};rows.append(row)
  with (a.output/'progress.jsonl').open('a') as f:f.write(json.dumps(row)+'\n')
  print(str(len(rows))+' '+label,flush=True);return v
 def reject(fn,reason=None):
  try:fn()
  except (ValueError,TypeError,KeyError) as e:
   if reason is not None:assert str(e)==reason,(str(e),reason)
   return True
  raise AssertionError('Unexpected acceptance')
 try:
  m=module(a.root/'code/correspondence.py');data=m.inputs(a.root);cat=check('source-derived state catalogue',lambda:m.catalogue(data));c=data['coverage'];d=m.inner(data);g=d['guards']
  tree=ast.parse(d['manager']);cls=next(n for n in tree.body if isinstance(n,ast.ClassDef) and n.name=='ManagedAuthority');methods={n.name:n for n in cls.body if isinstance(n,ast.FunctionDef)};run=methods['_run'];w=methods['state'];lock=run.body[0];tr=lock.body[1]
  check('independent AST state selection and direct result forwarding',lambda:ast.literal_eval(w.body[0].value.args[0])=='state' and ast.unparse(tr.body[1].value)=='getattr(self._live, method)(*args)' and ast.unparse(tr.body[-1].value)==cat['source']['result_local'])
  check('readiness outside try and exit outside handler',lambda:isinstance(lock.body[0],ast.Expr) and ast.unparse(lock.body[0].value)=='self._require()' and isinstance(tr,ast.Try) and tr.lineno>lock.body[0].lineno and cat['source']['outside_handler']==['lock_enter','readiness','lock_exit'])
  claims=check('pristine semantic',lambda:m.semantic(data,cat));bundle=check('pristine derivation',lambda:m.derive_state(data,cat));saved=m.enc(bundle);receipt=a.root/'results/state-correspondence.json'
  if a.write:
   with receipt.open('xb') as f:f.write(saved)
  else:assert receipt.read_bytes()==saved
  check('pristine public mandatory validator',lambda:m.validate(a.root,saved))
  prior=json.loads((a.root/'retained/config/results/config-correspondence.json').read_bytes())
  normal={'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'normal','post_transaction':False,'return_expression':'normal','lock_exit':'normal'}
  for i,row in enumerate(claims):
   name=row['context'];anchor=row['validated_state_anchor'];state=anchor['validated_state'];scope=m.reference_scope(anchor);live={'kind':'authority-reference','scope':copy.deepcopy(scope),'symbol':'rho-live'};ref={'kind':'state-result-reference','scope':copy.deepcopy(scope),'symbol':'rho-state'}
   projection={'method':'state','args':[],'phase':'READY','live_reference':live,'retired_reference':None,'outcomes':dict(normal),
    'underlying':{'receiver':copy.deepcopy(live),'value':copy.deepcopy(state),'reference':copy.deepcopy(ref)},'run_result':{'value':copy.deepcopy(state),'reference':copy.deepcopy(ref)},'wrapper_return':{'value':copy.deepcopy(state),'reference':copy.deepcopy(ref)}}
   case={'kind':'CONSTRUCTED-CONDITIONAL-STATE','context':name,'anchor':copy.deepcopy(anchor),'projection':projection}
   result=check('instance-qualified constructed forwarding '+name,lambda case=case:m.constructed_projection(data,cat,case));cases.append(result)
   old=prior['contexts'][i];now=bundle['contexts'][i];check('all predecessor context members unchanged '+name,lambda old=old,now=now:all(m.enc(now[k])==m.enc(v) for k,v in old.items()))
   check('sparse execution links and observer remain separate '+name,lambda row=row:row['runtime_links'] is None and row['actual_call_count'] is None and row['separate_observer']['frame'] is None and row['separate_observer']['joins_to_three_return_links'] is None and all(x['observed_value'] is None and x['object_reference_observed'] is None for x in row['conditional_links']))
   # Pure source/value algebra under the independently validated state premise.
   mutations=[('wrong method',lambda x:x.update(method='handle')),('extra arguments',lambda x:x.update(args=[1])),('wrong phase',lambda x:x.update(phase='CLOSED')),('retired present',lambda x:x.update(retired_reference=copy.deepcopy(live))),('wrong receiver',lambda x:x['underlying']['receiver'].update(symbol='other-live')),
    ('missing run link',lambda x:x.pop('run_result')),('copied run reference',lambda x:x['run_result']['reference'].update(symbol='copy')),('copied wrapper reference',lambda x:x['wrapper_return']['reference'].update(symbol='copy')),('wrong nested result type',lambda x:x['run_result']['value']['counts'].update(query=True)),('wrong nested result value',lambda x:x['wrapper_return']['value']['counts'].update(query=state['counts']['query']+1)),('wrong head',lambda x:x['underlying']['value'].update(head='f'*64))]
   for label,fn in mutations:
    bad=copy.deepcopy(projection);fn(bad);check('projection rejects '+label+' '+name,lambda bad=bad:reject(lambda:c.state_value_projection(cat,bad,state)))
   other=copy.deepcopy(projection)
   for k in ('underlying','run_result','wrapper_return'):other[k]['reference']['symbol']='another-constructed-state'
   check('alternative consistent constructed symbol without physical identity claim '+name,lambda other=other:not c.state_value_projection(cat,other,state)['actual_object_identity_established'])
   bad=copy.deepcopy(claims);bad[i]['conditional_links'].pop(1);check('semantic omitted correspondence link '+name,lambda bad=bad:reject(lambda:m.semantic(data,cat,bad),'STATE-LINK-COVERAGE'))
   bad=copy.deepcopy(claims);bad[i]['validated_state_anchor']['instance']['managed_constructor_frame']+=1;check('derivation wrong-instance anchor '+name,lambda bad=bad:reject(lambda:m.derive_state(data,cat,bad),'STATE-ANCHOR-LINEAGE'))
   if not a.recovered:
    bad=copy.deepcopy(case);bad['projection']['live_reference']['scope']['instance']['managed_constructor_frame']+=1;bad['projection']['underlying']['receiver']=copy.deepcopy(bad['projection']['live_reference'])
    check('constructed wrong-instance reference scope '+name,lambda bad=bad:reject(lambda:m.constructed_projection(data,cat,bad),'STATE-CASE-REFERENCE-SCOPE'))
  # Constructed exceptional paths derive transitions from source stage regions.
  specs=[('lock entry',{'lock_enter':'raise'},'lock_enter',False,None),
   ('readiness',{'lock_enter':'normal','readiness':'raise','lock_exit':'normal'},'readiness',False,None),
   ('pre active',{'lock_enter':'normal','readiness':'normal','pre_transaction':True,'handler_reason':'normal','quarantine':'normal','lock_exit':'normal'},'pre_transaction',True,True),
   ('dispatch',{'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'raise','handler_reason':'normal','quarantine':'normal','lock_exit':'normal'},'dispatch',True,True),
   ('post active',{'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'normal','post_transaction':True,'handler_reason':'normal','quarantine':'normal','lock_exit':'normal'},'post_transaction',True,True),
   ('reason failure',{'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'raise','handler_reason':'raise','lock_exit':'normal'},'handler_reason',False,None),
   ('quarantine interruption',{'lock_enter':'normal','readiness':'normal','pre_transaction':False,'dispatch':'raise','handler_reason':'normal','quarantine':'raise','lock_exit':'normal'},'quarantine',True,False),
   ('exit overrides return',dict(normal,lock_exit='raise'),'lock_exit',False,None)]
  for label,outcomes,failure,called,completed in specs:
   path=c.state_path_projection(cat,outcomes);paths.append(path)
   check('source exceptional region '+label,lambda path=path,failure=failure,called=called,completed=completed:path['completion']=='abrupt' and path['failure_site']==failure and path['quarantine_called'] is called and path['quarantine_completed'] is completed and not path['return_links_admissible'])
   bad=copy.deepcopy(cases[0]);proj=copy.deepcopy(projection);proj['outcomes']=outcomes
   check('abrupt path cannot claim normal links '+label,lambda proj=proj:reject(lambda:c.state_value_projection(cat,proj,state),'STATE-NO-NORMAL-RETURN'))
  check('normal path has no quarantine',lambda:c.state_path_projection(cat,normal)['quarantine_called'] is False)
  check('unreached dispatch outcome rejects',lambda:reject(lambda:c.state_path_projection(cat,{'lock_enter':'raise','dispatch':'normal'}),'STATE-PATH-UNREACHED-OUTCOMES'))
  check('integer cannot impersonate boolean transaction state',lambda:reject(lambda:c.state_path_projection(cat,dict(normal,pre_transaction=0))))
  # Catalogue expectation is derived independently from defining sources.
  def validate_cat(bad):
   return c.validate_state_return(d['manager'],d['authority'],d['ctx']['c']['retained/candidate/compiler/managed_observations.py'],d['values']['candidate/managed-route/model.json'],d['values']['candidate/managed-route/producers.json'],g['guard_relationships'],g['guard_oracle'],d['reference_module'].reference_catalogue(d),bad)
  mutations=[('omitted static link',lambda x:x['links'].pop()),('wrong selector',lambda x:x['source'].update(method='handle')),('omitted guard',lambda x:x['source']['run_return'].update(guards=[])),('false exit quarantine',lambda x:x['source']['caught_stages'].append('lock_exit')),('false copy',lambda x:x['links'][0].update(kind='deepcopy')),('wrong HEAD type',lambda x:x['inherited_head']['native_template']['type']['object'].update(seq='BOOLEAN')),('wrong origin',lambda x:x['declarations'][1]['origin'].update(expression='result=self._retired.state()'))]
  for label,fn in mutations:
   bad=copy.deepcopy(cat);fn(bad);check('source oracle rejects '+label,lambda bad=bad:reject(lambda:validate_cat(bad)))
  bad=copy.deepcopy(cat);bad['source']['method']='handle';bad['delegation']['to']='Authority.handle';bad['source']['wrapper_call']['expression']="self._run('handle')"
  check('coordinated source substitution rejected by semantic',lambda:reject(lambda:m.semantic(data,bad),'STATE-SOURCE-CATALOGUE'))
  evidence=d['ctx']['e'];old=json.loads(bytes.fromhex(json.loads(evidence['evidence/recovery-export-0.json'])['head']))['head'];new='f'*64
  changes=[];altered={}
  def replace(v):
   if type(v) is str:
    if v==old:return new
    try:raw=bytes.fromhex(v);decoded=json.loads(raw)
    except (ValueError,UnicodeError):return v
    changed=replace(decoded)
    return (json.dumps(changed,sort_keys=True,separators=(',',':')).encode().hex() if changed!=decoded else v)
   if type(v) is list:return [replace(x) for x in v]
   if type(v) is dict:return {k:replace(x) for k,x in v.items()}
   return v
  for n,b in evidence.items():
   out=b
   if n.endswith('.json'):
    value=json.loads(b);changed=replace(value)
    if changed!=value:out=m.enc(changed)
   altered[n]=out
   if out!=b:changes.append({'path':n,'before':identity(b),'after':identity(out)})
  (a.output/'coordinated-substitution.json').write_bytes(m.enc(changes))
  check('semantic coordinated saved HEAD substitutions',lambda:reject(lambda:m.semantic(data,cat,evidence=altered),'STATE-VALUE-ORIGIN:/head'))
  check('derivation coordinated saved HEAD substitutions',lambda:reject(lambda:m.derive_state(data,cat,evidence=altered),'STATE-VALUE-ORIGIN:/head'))
  bad=copy.deepcopy(claims)
  for row in bad:
   row['validated_state_anchor']['validated_state']['head']=new
   for link in row['conditional_links']:link['conditional_value_at_validated_frontier']['head']=new
  check('coordinated three returned values cannot redefine expectation',lambda:reject(lambda:m.derive_state(data,cat,bad),'STATE-VALUE-ORIGIN:/head'))
  if not a.recovered:
   for label,fn in [('wrong instance binding',lambda s:s.update(binding='f'*64)),('wrong nested type',lambda s:s['counts'].update(query=True)),('missing field',lambda s:s.pop('seq'))]:
    bad=dict(evidence);x=json.loads(bad['evidence/recovery-export-0.json']);v=json.loads(bytes.fromhex(x['head']));fn(v);x['head']=m.enc(v).hex();bad['evidence/recovery-export-0.json']=m.enc(x)
    check('semantic '+label,lambda bad=bad:reject(lambda:m.semantic(data,cat,evidence=bad)))
   bad=copy.deepcopy(claims);bad[0]['validated_state_anchor']['recovery_occurrence']='stale';check('stale frontier derivation',lambda:reject(lambda:m.derive_state(data,cat,bad),'STATE-ANCHOR-LINEAGE'))
  bad=copy.deepcopy(bundle);bad['contexts'][0].pop('state_return_correspondence');check('public missing mandatory mapping',lambda:reject(lambda:m.validate(a.root,m.enc(bad))))
  pristine=m.enc(claims);second=m.enc(claims[1]);claims[0]['conditional_links'][0]['conditional_value_at_validated_frontier']['counts']['query']=99;claims[0]['declaration']['links'].clear()
  check('nested contexts isolated',lambda:m.enc(claims[1])==second)
  check('nested mutated semantic output rejected',lambda:reject(lambda:m.semantic(data,cat,claims)))
  check('pristine expectations survive result mutation',lambda:m.enc(m.semantic(data,cat))==pristine)
  bundle['contexts'].clear();check('public cleared contexts reject',lambda:reject(lambda:m.validate(a.root,m.enc(bundle))))
  check('pristine public remains valid',lambda:m.validate(a.root,saved))
  check('both contexts required',lambda:reject(lambda:m.semantic(data,cat,[]),'STATE-CONTEXT-DOMAIN'))
 except BaseException as ex:error=repr(ex);raise
 finally:
  result={'result':'PASS' if error is None else 'FAIL','checks':len(rows),'rows':rows,'error':error,'seconds':time.monotonic()-start,'mode':'recovered' if a.recovered else 'primary','source':{n:identity((a.root/'code'/n).read_bytes()) for n in ('managed_coverage.py','correspondence.py')},'actual_state_chain':'UNAVAILABLE','constructed_cases_are_runtime_observations':False,'database_connections':0,'session_operations':0,'host_execution':False,'completed_suites_rerun':False}
  (a.output/'RESULT.json').write_text(json.dumps(result,indent=2)+'\n');(a.output/'constructed-cases.json').write_text(json.dumps(cases,indent=2)+'\n');(a.output/'constructed-paths.json').write_text(json.dumps(paths,indent=2)+'\n');print(json.dumps({k:result[k] for k in ('result','checks','seconds','error')}),flush=True)
if __name__=='__main__':main()
